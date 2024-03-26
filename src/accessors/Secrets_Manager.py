import boto3
import json


def get_secret(key: str) -> str:
    clinic_shopify_token = boto3.client("secretsmanager").get_secret_value(
        SecretId=key
    )["SecretString"]
    return json.loads(clinic_shopify_token)[key]
