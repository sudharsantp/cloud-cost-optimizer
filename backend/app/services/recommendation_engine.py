import boto3
from datetime import datetime, timedelta, timezone


class RecommendationEngine:

    def __init__(self):

        session = boto3.session.Session()

        self.region = (
            session.region_name
            or "ap-south-1"
        )

        self.ec2 = boto3.client(
            "ec2",
            region_name=self.region
        )

        self.cloudwatch = boto3.client(
            "cloudwatch",
            region_name=self.region
        )

        self.analysis_warnings = []

        self.analysis = {
            "running_ec2_instances": 0,
            "ebs_volumes": 0,
            "unattached_ebs_volumes": 0,
            "elastic_ips": 0,
            "unused_elastic_ips": 0
        }

    # =========================================================
    # EC2
    # =========================================================

    def get_running_instances(self):

        response = self.ec2.describe_instances(
            Filters=[
                {
                    "Name": "instance-state-name",
                    "Values": ["running"]
                }
            ]
        )

        instances = []

        for reservation in response.get(
            "Reservations", []
        ):

            for instance in reservation.get(
                "Instances", []
            ):

                instances.append({
                    "instance_id":
                        instance["InstanceId"],

                    "instance_type":
                        instance["InstanceType"],

                    "state":
                        instance["State"]["Name"],

                    "launch_time":
                        instance.get("LaunchTime")
                })

        self.analysis[
            "running_ec2_instances"
        ] = len(instances)

        return instances

    # =========================================================
    # CLOUDWATCH CPU
    # =========================================================

    def get_cpu_utilization(
        self,
        instance_id
    ):

        end_time = datetime.now(
            timezone.utc
        )

        start_time = (
            end_time
            - timedelta(days=7)
        )

        try:

            response = (
                self.cloudwatch
                .get_metric_statistics(
                    Namespace="AWS/EC2",

                    MetricName="CPUUtilization",

                    Dimensions=[
                        {
                            "Name": "InstanceId",
                            "Value": instance_id
                        }
                    ],

                    StartTime=start_time,
                    EndTime=end_time,

                    Period=3600,

                    Statistics=["Average"]
                )
            )

            datapoints = response.get(
                "Datapoints",
                []
            )

            if not datapoints:
                return None

            values = [
                point["Average"]
                for point in datapoints
                if "Average" in point
            ]

            if not values:
                return None

            return round(
                sum(values) / len(values),
                2
            )

        except Exception as e:

            self.analysis_warnings.append(
                f"CloudWatch CPU analysis failed "
                f"for {instance_id}: {str(e)}"
            )

            return None

    # =========================================================
    # EC2 OPTIMIZATION
    # =========================================================

    def analyze_ec2(self):

        recommendations = []

        try:

            instances = (
                self.get_running_instances()
            )

        except Exception as e:

            self.analysis_warnings.append(
                f"EC2 analysis failed: {str(e)}"
            )

            return recommendations

        for instance in instances:

            cpu = self.get_cpu_utilization(
                instance["instance_id"]
            )

            if cpu is None:
                continue

            # Underutilized EC2:
            # average CPU < 10% over 7 days

            if cpu < 10:

                recommendations.append({

                    "type":
                        "UNDERUTILIZED_EC2",

                    "priority":
                        "HIGH",

                    "service":
                        "EC2",

                    "resource_id":
                        instance["instance_id"],

                    "resource_type":
                        instance["instance_type"],

                    "reason": (
                        f"Average CPU utilization is "
                        f"{cpu}% over the last 7 days."
                    ),

                    "metric": {
                        "cpu_utilization": cpu
                    },

                    "estimated_monthly_savings":
                        0,

                    "action": (
                        "Consider stopping or "
                        "rightsizing this instance."
                    )
                })

        return recommendations

    # =========================================================
    # EBS
    # =========================================================

    def analyze_ebs(self):

        recommendations = []

        try:

            response = self.ec2.describe_volumes()

            volumes = response.get(
                "Volumes",
                []
            )

            self.analysis[
                "ebs_volumes"
            ] = len(volumes)

            for volume in volumes:

                # "available" means the volume
                # is not attached to an instance.

                if volume.get("State") == "available":

                    self.analysis[
                        "unattached_ebs_volumes"
                    ] += 1

                    recommendations.append({

                        "type":
                            "UNATTACHED_EBS",

                        "priority":
                            "MEDIUM",

                        "service":
                            "EBS",

                        "resource_id":
                            volume["VolumeId"],

                        "resource_type":
                            "EBS Volume",

                        "reason": (
                            f"EBS volume of "
                            f"{volume.get('Size', 0)} GB "
                            f"is currently unattached."
                        ),

                        "metric": {
                            "size_gb":
                                volume.get(
                                    "Size",
                                    0
                                )
                        },

                        "estimated_monthly_savings":
                            0,

                        "action": (
                            "Review and delete the "
                            "volume if it is no longer "
                            "required."
                        )
                    })

        except Exception as e:

            self.analysis_warnings.append(
                f"EBS analysis failed: {str(e)}"
            )

        return recommendations

    # =========================================================
    # ELASTIC IP
    # =========================================================

    def analyze_elastic_ips(self):

        recommendations = []

        try:

            response = (
                self.ec2.describe_addresses()
            )

            addresses = response.get(
                "Addresses",
                []
            )

            self.analysis[
                "elastic_ips"
            ] = len(addresses)

            for address in addresses:

                # No InstanceId means the address
                # is not associated with an EC2 instance.

                if not address.get("InstanceId"):

                    self.analysis[
                        "unused_elastic_ips"
                    ] += 1

                    recommendations.append({

                        "type":
                            "UNUSED_ELASTIC_IP",

                        "priority":
                            "LOW",

                        "service":
                            "EC2",

                        "resource_id":
                            address.get(
                                "AllocationId",
                                address.get(
                                    "PublicIp",
                                    "unknown"
                                )
                            ),

                        "resource_type":
                            "Elastic IP",

                        "reason": (
                            "Elastic IP is not "
                            "currently associated "
                            "with an EC2 instance."
                        ),

                        "metric": {},

                        "estimated_monthly_savings":
                            0,

                        "action": (
                            "Release the Elastic IP "
                            "if it is no longer required."
                        )
                    })

        except Exception as e:

            self.analysis_warnings.append(
                f"Elastic IP analysis failed: {str(e)}"
            )

        return recommendations

    # =========================================================
    # MAIN ANALYSIS
    # =========================================================

    def generate_recommendations(self):

        # Reset values every time the API is called.

        self.analysis_warnings = []

        self.analysis = {
            "running_ec2_instances": 0,
            "ebs_volumes": 0,
            "unattached_ebs_volumes": 0,
            "elastic_ips": 0,
            "unused_elastic_ips": 0
        }

        recommendations = []

        # EC2
        recommendations.extend(
            self.analyze_ec2()
        )

        # EBS
        recommendations.extend(
            self.analyze_ebs()
        )

        # Elastic IP
        recommendations.extend(
            self.analyze_elastic_ips()
        )

        # Calculate total savings.

        estimated_monthly_savings = sum(
            float(
                recommendation.get(
                    "estimated_monthly_savings",
                    0
                ) or 0
            )
            for recommendation
            in recommendations
        )

        return {

            "generated_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "data_source":
                "AWS",

            "region":
                self.region,

            "analysis":
                self.analysis,

            "recommendation_count":
                len(recommendations),

            "estimated_monthly_savings":
                round(
                    estimated_monthly_savings,
                    2
                ),

            "analysis_warnings":
                self.analysis_warnings,

            "recommendations":
                recommendations
        }


# Optional global instance.
# Existing code using RecommendationEngine()
# will continue to work.

engine = RecommendationEngine()