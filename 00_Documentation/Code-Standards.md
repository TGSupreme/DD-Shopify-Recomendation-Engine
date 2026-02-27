# Recommendation Engine: Codebase Structure & Development Standards

## 1. Project Directory Structure
The project is designed for high modularity to ensure compatibility with future scaling requirements. Each component is isolated to allow for easy swapping of AI models, vector databases, or recommendation algorithms without core logic changes.

```text
recommendation-engine/
├── app/
│   ├── main.py              # Application entry point & FastAPI initialization
│   ├── api/                 # API Layer (Routes & Dependencies)
│   │   ├── deps.py          # Dependency injection (Service instances)
│   │   └── v1/
│   │       ├── sync.py      # Product synchronization endpoints
│   │       ├── recommend.py # User & Product recommendation endpoints
│   │       └── search.py    # Semantic search endpoints
│   ├── core/                # Global Configuration
│   │   ├── config.py        # Environment variables & Pydantic settings
│   │   └── constants.py     # Default weights, model names, and fixed values
│   ├── schemas/             # Data Validation (Pydantic Models)
│   │   ├── product.py       # Shopify/Express product schema
│   │   ├── history.py       # User behavior (Viewed/Bought/Cart) schema
│   │   └── response.py      # Standardized API response formats
│   ├── services/            # Business Logic (The "Brain")
│   │   ├── embedding/       # LangChain Embedding Providers
│   │   │   ├── factory.py   # Model switcher (OpenAI/Gemini)
│   │   │   └── base.py      # Abstract base class for providers
│   │   ├── vector_store/    # Pinecone Integration
│   │   │   └── client.py    # Vector CRUD operations
│   │   ├── recommender/     # Recommendation Strategies
│   │   │   ├── base.py      # Strategy Interface
│   │   │   ├── user.py      # Personalization logic (Weighted Averaging)
│   │   │   └── item.py      # Similarity logic (Related products)
│   │   └── processors/      # Logic Workers
│   │       ├── profile.py   # User Interest Vector calculation (NumPy)
│   │       └── reranker.py  # Post-query filtering & business logic
│   ├── utils/               # Shared Helpers
│   │   ├── formatter.py     # JSON-to-String text formatting
│   │   └── math_ops.py      # NumPy normalization and vector math
├── tests/                   # Unit & Integration Tests
├── .env                     # Configuration (Not tracked in Git)
├── requirements.txt         # Dependency manifest
└── README.md
```

---

## 2. Coding Rules & Regulations

### A. Modular Design (The "Plug-and-Play" Rule)
*   **No Hardcoding:** Never hardcode API keys or model names. Use `app/core/config.py`.
*   **Interface First:** All services (Embedding, VectorStore, Recommender) must inherit from an Abstract Base Class (ABC) to ensure swapping components doesn't break the system.
*   **Single Responsibility:** A route should only handle the request; the `recommender` service handles the logic; the `processor` handles the math.

### B. Technical Standards
*   **Type Hinting:** Mandatory use of Python type hints (`name: str`, `vector: np.ndarray`) for better IDE support and error catching.
*   **Async/Await:** Use `async` for all I/O bound operations (Pinecone queries, API calls to OpenAI/Gemini) to ensure the FastAPI server remains responsive.
*   **Statelessness:** The server must not store any local state. Every request must be fulfilled using the data provided in the payload and the external vector database.

### C. Math & Performance
*   **NumPy Only:** All vector operations (averaging, weighting, normalization) must be performed using NumPy for speed.
*   **Normalization:** Always normalize vectors before sending them to Pinecone or performing weighted math to maintain Cosine Similarity accuracy.

### D. Data Integrity (The "Validation" Rule)
*   **Pydantic Models:** Every incoming JSON from the Express server must be validated against a Pydantic schema in `app/schemas/`.
*   **Fail Gracefully:** If an embedding model fails, the system should return a clear error code or fallback to a simpler "Popular Items" recommendation if applicable.

---

## 3. Development Workflow

1.  **Define Schema:** Update `app/schemas/` if the Express server adds new fields to the user history or product data.
2.  **Update Formatter:** Ensure `app/utils/formatter.py` includes new relevant fields in the text string used for embeddings.
3.  **Implement Logic:** Add/Update the specific strategy in `app/services/recommender/`.
4.  **Register Route:** Add the endpoint to `app/api/v1/`.
5.  **Test:** Run unit tests for the math logic in `app/services/processors/`.
