from fastapi import FastAPI
from app.api.v1 import sync, recommend, search, debug, products
from app.services.vector_store import verify_pinecone_connection

app = FastAPI(title="Recommendation Engine Service")

@app.on_event("startup")
async def startup_event():
    """Verify core service connections on startup."""
    verify_pinecone_connection()
    print("Pinecone connection verified successfully.")

# Include Routers
app.include_router(sync.router, prefix="/v1/sync", tags=["sync"])
app.include_router(recommend.router, prefix="/v1/recommend", tags=["recommend"])
app.include_router(search.router, prefix="/v1/search", tags=["search"])
app.include_router(products.router, prefix="/v1/products", tags=["products"])
app.include_router(debug.router, prefix="/debug", tags=["debug"])

@app.get("/")
async def root():
    return {"message": "Recommendation Engine Service is running."}
