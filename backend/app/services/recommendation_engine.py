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
        instance_id,
        launch_time=None
    ):

        end_time = datetime.now(
            timezone.utc
        )

        # -----------------------------------------------------
        # Use the instance launch time when available.
        #
        # This prevents a newly launched instance from being
        # incorrectly described as having "7 days" of data.
        # -----------------------------------------------------

        default_start = (
            end_time - timedelta(days=7)
        )

        if launch_time:

            if launch_time.tzinfo is None:
                launch_time = launch_time.replace(
                    tzinfo=timezone.utc
                )

            start_time = max(
                launch_time,
                default_start
            )

        else:

            start_time = default_start

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

            return {
                "average_cpu": round(
                    sum(values) / len(values),
                    2
                ),

                "datapoint_count": len(values),

                "start_time": start_time,

                "end_time": end_time
            }

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

            cpu_data = self.get_cpu_utilization(
                instance["instance_id"],
                instance.get("launch_time")
            )

            if cpu_data is None:
                continue

            cpu = cpu_data["average_cpu"]

            datapoint_count = (
                cpu_data["datapoint_count"]
            )

            launch_time = instance.get(
                "launch_time"
            )

            # -------------------------------------------------
            # Determine the actual measurement period.
            # -------------------------------------------------

            if launch_time:

                if launch_time.tzinfo is None:
                    launch_time = launch_time.replace(
                        tzinfo=timezone.utc
                    )

                age = (
                    datetime.now(timezone.utc)
                    - launch_time
                )

                age_days = max(
                    age.total_seconds() / 86400,
                    0
                )

            else:

                age_days = 7

            # -------------------------------------------------
            # Human-readable measurement period
            # -------------------------------------------------

            if age_days < 1:

                measurement_period = (
                    "the available CloudWatch "
                    "datapoints since launch"
                )

            elif age_days < 7:

                measurement_period = (
                    f"the available CloudWatch "
                    f"datapoints from the last "
                    f"{age_days:.1f} days"
                )

            else:

                measurement_period = (
                    "the available CloudWatch "
                    "datapoints over the last 7 days"
                )

            # -------------------------------------------------
            # UNDERUTILIZED EC2
            # -------------------------------------------------

            if cpu < 10:

                recommendations.append({

                    "type":
                        "UNDERUTILIZED_EC2",

                    "priority":
                        "MEDIUM",

                    "service":
                        "EC2",

                    "resource_id":
                        instance["instance_id"],

                    "resource_type":
                        instance["instance_type"],

                    "reason": (
                        f"Average CPU utilization is "
                        f"{cpu:.2f}% based on "
                        f"{measurement_period}, "
                        f"indicating low CPU utilization."
                    ),

                    "metric": {

                        "cpu_utilization":
                            cpu,

                        "datapoints":
                            datapoint_count,

                        "measurement_period":
                            measurement_period
                    },

                    "estimated_monthly_savings":
                        None,

                    "action": (
                        "Review whether this instance "
                        "is required continuously. "
                        "If it is used only for testing "
                        "or development, stop it when "
                        "not in use. If it is a persistent "
                        "workload, evaluate rightsizing "
                        "based on sustained CPU, memory, "
                        "and workload requirements."
                    ),

                    "detection_method":
                        "CloudWatch CPU utilization"
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
                            None,

                        "action": (
                            "Review and delete the "
                            "volume if it is no longer "
                            "required."
                        ),

                        "detection_method":
                            "AWS EC2 resource analysis"
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
                            None,

                        "action": (
                            "Release the Elastic IP "
                            "if it is no longer required."
                        ),

                        "detection_method":
                            "AWS EC2 resource analysis"
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

        self.analysis_warnings = []

        self.analysis = {
            "running_ec2_instances": None,
            "ebs_volumes": None,
            "unattached_ebs_volumes": None,
            "elastic_ips": None,
            "unused_elastic_ips": None
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

        # -----------------------------------------------------
        # Calculate savings only when an actual numeric value
        # exists.
        # -----------------------------------------------------

        numeric_savings = [
            float(
                recommendation[
                    "estimated_monthly_savings"
                ]
            )

            for recommendation
            in recommendations

            if isinstance(
                recommendation.get(
                    "estimated_monthly_savings"
                ),
                (int, float)
            )
        ]

        estimated_monthly_savings = sum(
            numeric_savings
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

engine = RecommendationEngine()