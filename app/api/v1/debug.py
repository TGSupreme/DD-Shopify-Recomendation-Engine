from fastapi import APIRouter, Request
import logging
import json
from app.schemas.product import ProductOption, Product

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("")
@router.post("/")
async def log_request(request: Request):
    """
    Receives Shopify webhook and logs a structured Product object.
    """

    try:
        body = await request.json()
        headers = dict(request.headers)

        # -------- extract fields --------

        store_id = headers.get("x-shopify-shop-domain")

        product_id = str(body.get("id"))

        title = body.get("title")

        product_type = body.get("product_type")

        vendor = body.get("vendor")

        # tags come as comma separated string
        tags_str = body.get("tags", "")
        tags = [t.strip() for t in tags_str.split(",")] if tags_str else []

        # options -> ProductOption objects
        options = [
            ProductOption(name=o["name"], values=o["values"])
            for o in body.get("options", [])
        ]

        # first variant price
        variants = body.get("variants", [])
        price = float(variants[0]["price"]) if variants else 0.0

        # -------- create Product object --------

        product = Product(
            id=product_id,
            store_id=store_id,
            title=title,
            product_type=product_type,
            vendor=vendor,
            tags=tags,
            options=options,
            price=price,
        )

        logger.info(f"Parsed product: {product.model_dump()}")

        return {
            "status": "success",
            "product": product.model_dump()
        }

    except Exception as e:
        raw_body = await request.body()
        decoded_body = raw_body.decode("utf-8", errors="replace")

        logger.error(f"Webhook parsing failed: {str(e)}")
        logger.info(f"Raw body: {decoded_body}")

        return {
            "status": "error",
            "message": str(e)
        }

@router.get("")
@router.get("/")
async def log_get_request(request: Request):
    """
    Receives a GET request and logs its query parameters.
    """
    params = dict(request.query_params)
    logger.info(f"DEBUG: Received GET request with params: {params}")
    return {"status": "success", "params": params}

