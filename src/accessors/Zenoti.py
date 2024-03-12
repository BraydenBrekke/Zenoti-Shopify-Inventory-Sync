import requests
import difflib
import json


class Zenoti:
    def __init__(self):
        try:
            payload = json.dumps(
                {
                    "account_name": "options",
                    "user_name": "bbrekke",
                    "password": "kewboq-rovged-7zuXky",
                    "grant_type": "password",
                    "app_id": "84EA22FC-4EE4-4801-803A-9332C365E83B",
                    "app_secret": "c5913b53d97e4b64add8fbc69857833044a99f9df2644c37b32cd221acd90e6e",  # noqa
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
                }
            )
            products = response.json()['list']
            if products:
                return products[0]
        except requests.exceptions.RequestException as e:
            print(e)
