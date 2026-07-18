import boto3
import os
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError
from app.models import CostRecord
from app.database import SessionLocal


def fetch_aws_cost_and_usage(start_date: str, end_date: str, granularity="DAILY"):
    """
    Fetch AWS billing data from Cost Explorer
    and store it into the local database.
    """

    try:
        client = boto3.client(
            "ce",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )

        response = client.get_cost_and_usage(
            TimePeriod={
                "Start": start_date,
                "End": end_date
            },
            Granularity=granularity,
            Metrics=[
                "UnblendedCost",
                "UsageQuantity"
            ],
            GroupBy=[
                {
                    "Type": "DIMENSION",
                    "Key": "SERVICE"
                }
            ]
        )

        db = SessionLocal()

        for result in response["ResultsByTime"]:

            billing_date = datetime.strptime(
                result["TimePeriod"]["Start"],
                "%Y-%m-%d"
            ).date()

            billing_period_start = datetime.strptime(
                result["TimePeriod"]["Start"],
                "%Y-%m-%d"
            ).date()

            billing_period_end = datetime.strptime(
                result["TimePeriod"]["End"],
                "%Y-%m-%d"
            ).date()

            for group in result["Groups"]:

                service = group["Keys"][0]

                amount = float(
                    group["Metrics"]["UnblendedCost"]["Amount"]
                )

                usage = float(
                    group["Metrics"]["UsageQuantity"]["Amount"]
                )

                # Prevent duplicate records
                existing = db.query(CostRecord).filter(
                    CostRecord.billing_date == billing_date,
                    CostRecord.service == service
                ).first()

                if existing:
                    continue

                cost_record = CostRecord(
                    billing_date=billing_date,
                    service=service,
                    region="Global",
                    amount=amount,
                    usage=usage,
                    currency="USD",
                    granularity=granularity,
                    billing_period_start=billing_period_start,
                    billing_period_end=billing_period_end,
                    user_id=1
                )

                db.add(cost_record)

        db.commit()
        db.close()

        return {
            "status": "success",
            "message": "AWS billing data synchronized successfully."
        }

    except NoCredentialsError:
        return {
            "status": "error",
            "message": "AWS credentials not found."
        }

    except ClientError as e:
        return {
            "status": "error",
            "message": str(e)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }