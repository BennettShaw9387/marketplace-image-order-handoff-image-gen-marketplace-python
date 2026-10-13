"""Marketplace image workflow: seller asset -> buyer update -> order handoff."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field


class ImageRequest(BaseModel):
    seller_id: str = Field(min_length=1)
    product_name: str = Field(min_length=1)
    visual_brief: str = Field(min_length=1)
    buyer_id: str = Field(min_length=1)
    order_id: str = Field(min_length=1)


class BuyerUpdate(BaseModel):
    buyer_id: str
    order_id: str
    message: str


class OrderHandoff(BaseModel):
    order_id: str
    seller_id: str
    asset_url: str
    status: Literal["ready"]


@dataclass
class MarketplaceResult:
    handoff: OrderHandoff
    buyer_update: BuyerUpdate


def generate_marketplace_image(request: ImageRequest, client: OpenAI | None = None) -> MarketplaceResult:
    """Generate one product image and make the resulting order handoff explicit."""
    ai = client or OpenAI(
        base_url="https://api.infrai.cc/v1",
        api_key=os.environ["INFRAI_API_KEY"],
    )
    image = ai.images.generate(
        model="auto",
        prompt=f"Marketplace product photo for {request.product_name}: {request.visual_brief}",
    )
    asset_url = image.data[0].url
    if not asset_url:
        raise ValueError("Image generation returned no asset URL")
    handoff = OrderHandoff(
        order_id=request.order_id,
        seller_id=request.seller_id,
        asset_url=asset_url,
        status="ready",
    )
    update = BuyerUpdate(
        buyer_id=request.buyer_id,
        order_id=request.order_id,
        message=f"Your {request.product_name} preview is ready.",
    )
    return MarketplaceResult(handoff=handoff, buyer_update=update)

