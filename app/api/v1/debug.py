from fastapi import APIRouter, Request
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("")
@router.post("/")
async def log_request(request: Request):
    """
    Receives a request and logs its content (JSON body).
    """
    try:
        body = await request.json()
        logger.info(f"DEBUG: Received POST request: {json.dumps(body)}")
        return {"status": "success", "received": body}
    except Exception as e:
        # Fallback if body is not JSON or is empty
        raw_body = await request.body()
        decoded_body = raw_body.decode('utf-8', errors='replace')
        logger.info(f"DEBUG: Received non-JSON or empty POST request: {decoded_body}")
        return {"status": "success", "received_raw": decoded_body}

@router.get("")
@router.get("/")
async def log_get_request(request: Request):
    """
    Receives a GET request and logs its query parameters.
    """
    params = dict(request.query_params)
    logger.info(f"DEBUG: Received GET request with params: {params}")
    return {"status": "success", "params": params}

