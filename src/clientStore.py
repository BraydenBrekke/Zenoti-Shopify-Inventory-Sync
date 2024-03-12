from accessors.Shopify import Shopify
from accessors.Zenoti import Zenoti


clinic_shopify_token = "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"
clinic_url = "options-medical-weight-loss"


def handler(event, context):
    shopify = Shopify(clinic_url, clinic_shopify_token)
    zenoti = Zenoti()
    shopify_locations = shopify.get_inventory_locations()
    for shopify_location in shopify_locations:
        print("[syncing location " + shopify_location["name"] + "]")
        shopify_levels = shopify.get_inventory_levels(shopify_location["id"])
        zenoti_center_id = zenoti.get_center_id_from_center_name(
            shopify_location["name"]
        )
        for shopify_level in shopify_levels:
            shopify_item = shopify.get_inventory_item(
                shopify_level["inventory_item_id"]
            )
            if shopify_item["sku"]:
                zenoti_product = zenoti.get_stock_quantity_of_product(
                    zenoti_center_id, shopify_item["sku"]
                )
                if zenoti_product:
                    # shopify.set_inventory_item_level(
                    # shopify_item["id"],
                    # shopify_location["id"],
                    # zenoti_product["total_quantity"],
                    # )
                    print(" synced " + zenoti_product["product_name"])
                else:
                    print("ERROR: no match for " + shopify_item["sku"])
        print("[synced location " + shopify_location["name"] + "]")


handler(None, None)
