import requests


class Shopify:
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def get_inventory_locations(self):
        try:
            response = requests.request(
                "GET",
                f"https://{self.url}.myshopify.com/admin/api/2023-10/locations.json",
                headers={"X-Shopify-Access-Token": self.token},
            )
            return response.json()["locations"]
        except requests.exceptions.RequestException as e:
            print(e)

    def get_inventory_levels(self, location_id):
        try:
            response = requests.request(
                "GET",
                f"https://{self.url}.myshopify.com/admin/api/2023-10/inventory_levels.json?location_ids="
                + str(location_id),
                headers={"X-Shopify-Access-Token": self.token},
            )
            return response.json()["inventory_levels"]
        except requests.exceptions.RequestException as e:
            print(e)

    def get_inventory_item(self, item_id):
        try:
            response = requests.request(
                "GET",
                f"https://{self.url}.myshopify.com/admin/api/2023-10/inventory_items/{item_id}.json",
                headers={"X-Shopify-Access-Token": self.token},
            )
            return response.json()["inventory_item"]
        except requests.exceptions.RequestException as e:
            print(e)

    def set_inventory_item_level(self, item_id, location_id, quantity):
        try:
            response = requests.request(
                "POST",
                f"https://{self.url}.myshopify.com/admin/api/2023-10/inventory_levels/set.json",
                headers={"X-Shopify-Access-Token": self.token},
                json={
                    "location_id": location_id,
                    "inventory_item_id": item_id,
                    "available": quantity,
                },
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
