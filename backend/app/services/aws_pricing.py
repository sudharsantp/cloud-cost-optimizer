# aws_pricing.py
import boto3
import json


pricing = boto3.client(
    "pricing",
    region_name="us-east-1"
)


def get_ec2_hourly_price(
    instance_type: str,
    region: str
):
    response = pricing.get_products(
        ServiceCode="AmazonEC2",
        Filters=[
            {
                "Type": "TERM_MATCH",
                "Field": "instanceType",
                "Value": instance_type,
            },
            {
                "Type": "TERM_MATCH",
                "Field": "location",
                "Value": region,
            },
            {
                "Type": "TERM_MATCH",
                "Field": "operatingSystem",
                "Value": "Linux",
            },
            {
                "Type": "TERM_MATCH",
                "Field": "preInstalledSw",
                "Value": "NA",
            },
            {
                "Type": "TERM_MATCH",
                "Field": "capacitystatus",
                "Value": "Used",
            },
            {
                "Type": "TERM_MATCH",
                "Field": "tenancy",
                "Value": "Shared",
            },
        ],
        MaxResults=1,
    )

    if not response["PriceList"]:
        return None

    product = json.loads(response["PriceList"][0])

    terms = product["terms"]["OnDemand"]

    term = next(iter(terms.values()))

    dimension = next(
        iter(term["priceDimensions"].values())
    )

    return float(
        dimension["pricePerUnit"]["USD"]
    )