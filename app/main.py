from fastapi import FastAPI
from app.api.v1 import sync, recommend, search

app = FastAPI(title="Recommendation Engine Service")

# Include Routers
app.include_router(sync.router, prefix="/v1/sync", tags=["sync"])
app.include_router(recommend.router, prefix="/v1/recommend", tags=["recommend"])
app.include_router(search.router, prefix="/v1/search", tags=["search"])

@app.get("/")
async def root():
    return {"message": "Recommendation Engine Service is running."}
