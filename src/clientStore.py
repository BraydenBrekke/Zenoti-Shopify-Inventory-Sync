from accessors.Shopify import Shopify
from accessors.Zenoti import Zenoti
from accessors.Secrets_Manager import get_secret


def handler(event, context):
    clinic_shopify_token = get_secret("clinic_shopify_token")
    clinic_url = "options-medical-weight-loss"

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
            (
                shopify_product_barcode,
                shopify_product_title,
            ) = shopify.get_inventory_item_barcode_and_name(
                shopify_level["inventory_item_id"]
            )
            if shopify_product_barcode:
                zenoti_product = zenoti.get_stock_quantity_of_product(
                    zenoti_center_id, shopify_product_barcode
                )
                if zenoti_product:
                    # shopify.set_inventory_item_level(
                    # shopify_item["id"],
                    # shopify_location["id"],
                    # zenoti_product["total_quantity"],
                    # )
                    print(
                        " synced " + zenoti_product["product_name"]
                    )  # filter on only active products
                else:
                    print(
                        f'ERROR: no match in Zenoti for product "{shopify_product_title}" on shopify barcode {shopify_product_barcode}'
                    )
        print("[synced location " + shopify_location["name"] + "]")


handler(None, None)
