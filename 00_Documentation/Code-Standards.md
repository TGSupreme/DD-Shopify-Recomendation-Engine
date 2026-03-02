# Code Standards & Implementation Guide

## 1. Project Philosophy
**Simplicity First.** We prioritize functional, readable, and highly maintainable code. 
- **Avoid:** Classes, inheritance, factories, and Abstract Base Classes (ABCs).
- **Prefer:** Pure functions and clear module-level separation.
- **Asynchronous:** Every I/O operation (Pinecone, LangChain, FastAPI) **must** be `async`.

---

## 2. Directory Structure & Modularization
```text
app/
├── api/             # FastAPI Route Handlers
│   └── v1/          # Versioned API logic
├── core/            # Config (Pydantic Settings)
├── schemas/         # Request/Response validation (Pydantic)
├── services/        # Functional Business Logic
│   ├── embedding.py # LangChain wrappers
│   ├── recommender.py# Recommendation math and logic
│   └── vector_store.py# Pinecone operations
└── utils/           # Shared stateless helper functions
```

---

## 3. Implementation Patterns

### Global Client Singleton Pattern
To prevent re-initializing expensive SDK clients (like LangChain or Pinecone) on every request, we use a global variable with a getter function.

```python
_client = None

def get_client():
    global _client
    if _client is None:
        # Initialize only once
        _client = ExpensiveSDKClient(api_key=settings.API_KEY)
    return _client
```

### Namespace Enforcement
Every database call **must** accept a `namespace: str` parameter. This is the cornerstone of our multi-tenancy support for Shopify stores. 

```python
# Rule: No database call without a namespace
async def query_nearest(vector: np.ndarray, namespace: str, top_k: int = 10)
```

### Pure Function Utils
Helpers in `app/utils/` should be "Pure Functions": 
- No side effects (no API calls).
- Deterministic output based on inputs.
- Highly testable (unit tests).

---

## 4. Error Handling & Validation
- **Pydantic Validation:** All external data **must** be validated via Pydantic schemas in `app/schemas/`.
- **API Response:** Use the standardized `RecommendationResponse` and `SyncResponse` models from `app/schemas/response.py`.
- **Status Codes:**
    - `200 OK`: Successful sync or recommendation.
    - `500 Internal Server Error`: For any unexpected failures (Pinecone/OpenAI down).

---

## 5. Development Workflow
1.  **Sync:** Add products via `POST /v1/sync/` for a specific `store_id`.
2.  **Verify:** Check the logs or LangSmith to confirm the embedding and upsert occurred.
3.  **Recommend:** Test the personalization via `POST /v1/recommend/user` for that same `store_id`.
4.  **Validate:** Ensure the scores and product IDs returned match expectations.
