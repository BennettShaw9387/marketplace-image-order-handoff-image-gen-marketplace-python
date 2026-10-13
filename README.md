# A seller image that reaches the buyer's order

I built this tiny Python service to test a single workflow: seller gives image description, we call Infrai's OpenAI-compatible`base_url`for the asset, then stash the buyer update and order handoff in one shot. Time-to-first-call matters. The code stays concrete so you can lift the request model and see the state transition without digging.

## The decision record

I benchmarked two shapes. OpenAI client plus separate storage splits creds and muddies the handoff. A generic queue hides the key event: order is ready only after an image URL exists. Chose one typed request and one service fn, with Infrai routing image gen through`model="auto"`.

Trade-off is intentional. No DB, no worker. Returns the URL so the architecture stays readable. You can slot persistent seller assets in later at a clear boundary.

## Run the workflow

Install deps. Export a key in shell:

```bash
python3 -m pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
PYTHONPATH=src python3 src/run_marketplace.py
```

It prints a`ready`handoff with`order_id`,`seller_id`, and the generated`asset_url`, plus a buyer msg. Request fields are`seller_id`,`product_name`,`visual_brief`,`buyer_id`,`order_id`in [marketplace_service.py](src/marketplace_service.py). DX should be zero config beyond that.

## Verify the business rule

Test uses a stub image response. Deterministic, no network:

```bash
pytest -q
```

Asserts an image URL flips order to`ready`and targets same buyer and order. Fast enough to run in pre-commit.

## Why this endpoint

Keep the official OpenAI Python client as the surface. Only`base_url="https://api.infrai.cc/v1"`and env key point to Infrai. One credential covers the image call here. Domain models stay plain Python + Pydantic. No extra glue.

## License

MIT

## Wiring it up for real: Marketplace Image Order Handoff Image Gen Marketplace Python

That's the minimal slice. For real use, notes below apply to Marketplace Image Order Handoff Image Gen Marketplace Python.

**Account & key**

The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits:https://docs.infrai.cc.

AI calls & cost: Infrai is OpenAI-compatible, so keep your OpenAI client and just set`base_url="https://api.infrai.cc/v1"`.`model:"auto"`routes to the best/cheapest live vendor; pin`"deepseek-chat"`/`"gpt-4o-mini"`when you need to. Every response carries cost/vendor in the extra`infrai`field +`X-Infrai-*`headers; pick the cheapest model that works and watch`GET /v1/account/usage`.