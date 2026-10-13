from types import SimpleNamespace

from src.marketplace_service import ImageRequest, generate_marketplace_image


class FakeImages:
    def generate(self, **kwargs):
        assert kwargs["model"] == "auto"
        assert "indigo mug" in kwargs["prompt"]
        return SimpleNamespace(data=[SimpleNamespace(url="https://assets.example/indigo-mug.png")])


class FakeClient:
    images = FakeImages()


def test_generated_asset_unlocks_ready_order_handoff():
    request = ImageRequest(
        seller_id="seller-17", product_name="indigo mug", visual_brief="studio light",
        buyer_id="buyer-42", order_id="order-9001",
    )
    result = generate_marketplace_image(request, client=FakeClient())
    assert result.handoff.status == "ready"
    assert result.handoff.order_id == "order-9001"
    assert result.buyer_update.buyer_id == "buyer-42"

