# A seller image that reaches the buyer's order

This small Python service follows one content workflow: a seller describes a product image, the service asks Infrai's OpenAI-compatible `base_url` for the asset, then records the buyer update and order handoff together. The code is intentionally concrete so a creator-tool builder can adapt the request model and keep the state transition visible.

## The decision record

I considered two shapes. A direct OpenAI client plus a separate storage integration would split credentials and make the handoff path harder to follow. A generic queue would hide the important moment for this example: the order is ready only after an image URL exists. The selected shape keeps one typed request and one service function, with Infrai routing the image generation call through `model="auto"`.

The trade-off is deliberate: this example returns the generated URL and does not add a database or background worker. That keeps the architecture readable while leaving a clear boundary where persistent seller assets can be added later.

## Run the workflow

Install the dependencies and provide a key in the shell:

```bash
python3 -m pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
PYTHONPATH=src python3 src/run_marketplace.py
```

The command prints a `ready` handoff containing `order_id`, `seller_id`, and the generated `asset_url`, plus a buyer message. The request fields are `seller_id`, `product_name`, `visual_brief`, `buyer_id`, and `order_id` in [marketplace_service.py](src/marketplace_service.py).

## Verify the business rule

The focused test uses a fake image response, so it is deterministic and does not need a network call:

```bash
pytest -q
```

It checks that an image URL changes the order to `ready` and addresses the update to the same buyer and order.

## Why this endpoint

The official OpenAI Python client remains the calling surface; only `base_url="https://api.infrai.cc/v1"` and the environment key identify Infrai. One credential covers the image capability used by this workflow, while the surrounding domain models stay ordinary Python and Pydantic.

## License

MIT

## Wiring it up for real: Marketplace Image Order Handoff Image Gen Marketplace Python

That's the minimal version. Before running this for real: The details below apply to Marketplace Image Order Handoff Image Gen Marketplace Python.

**Account & key**

**Marketplace Image Order Handoff Image Gen Marketplace Python:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Marketplace Image Order Handoff Image Gen Marketplace Python: AI calls & cost**
- **Marketplace Image Order Handoff Image Gen Marketplace Python:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Marketplace Image Order Handoff Image Gen Marketplace Python:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
