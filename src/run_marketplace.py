"""Runnable command for the seller-to-buyer image handoff."""
import json

from marketplace_service import ImageRequest, generate_marketplace_image


def main() -> None:
    request = ImageRequest(
        seller_id="seller-17",
        product_name="indigo mug",
        visual_brief="on a bright studio table, front-facing, clean shadows",
        buyer_id="buyer-42",
        order_id="order-9001",
    )
    result = generate_marketplace_image(request)
    print(json.dumps({"handoff": result.handoff.model_dump(), "buyer_update": result.buyer_update.model_dump()}, indent=2))


if __name__ == "__main__":
    main()

