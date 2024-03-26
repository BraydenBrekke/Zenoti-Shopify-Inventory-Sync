import requests
import difflib
import json
import boto3
from accessors.Secrets_Manager import get_secret


class Zenoti:
    def __init__(self):
        try:
            zenoti_username = get_secret("zenoti_username")
            zenoti_password = get_secret("zenoti_password")
            zenoti_token = get_secret("zenoti_token")
            payload = json.dumps(
                {
                    "account_name": "options",
                    "user_name": zenoti_username,
                    "password": zenoti_password,
                    "grant_type": "password",
                    "app_id": "84EA22FC-4EE4-4801-803A-9332C365E83B",
                    "app_secret": zenoti_token,  # noqa
                    "device_id": "script",
                }
            )
            headers = {"Content-Type": "application/json"}

            token = requests.request(
                "POST",
                "https://api.zenoti.com/v1/tokens",
                headers=headers,
                data=payload,  # noqa
            ).json()["credentials"]["access_token"]
            self.token = token
        except requests.exceptions.RequestException as e:
            print(e)

    def get_center_id_from_center_name(self, shopify_location: str) -> str:  # noqa
        try:
            zenoti_centers = requests.get(
                "https://api.zenoti.com/v1/centers/",
                headers={
                    "accept": "application/json",
                    "Authorization": f"bearer {self.token}",
                },
            ).json()["centers"]
            zenoti_center_names = [
                zenoti_center["name"] for zenoti_center in zenoti_centers
            ]
            closest_zenoti_center = difflib.get_close_matches(
                shopify_location, zenoti_center_names, n=1, cutoff=0
            )[0]
            zenoti_center_id = [
                zenoti_center["id"]
                for zenoti_center in zenoti_centers
                if zenoti_center["name"] == closest_zenoti_center
            ]
            return zenoti_center_id[0]
        except requests.exceptions.RequestException as e:
            print(e)

    def get_stock_quantity_of_product(self, center_id, sku):
        try:
            response = requests.get(
                f"https://api.zenoti.com/v1/inventory/stock?center_id={center_id}&inventory_date=2024-03-07&search_string={sku}",
                headers={
                    "accept": "application/json",
                    "Authorization": f"bearer {self.token}",
                },
            )
            products = response.json()["list"]
            if products:
                return products[0]
        except requests.exceptions.RequestException as e:
            print(e)
