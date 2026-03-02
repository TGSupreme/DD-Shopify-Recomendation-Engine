# System Architecture - Source of Truth

## 1. Project Mission
A high-performance, multi-tenant recommendation service for the Shopify ecosystem. It provides semantic search and personalized "For You" recommendations by mapping user behavior and product data into a shared vector space.

---

## 2. Multi-tenancy via Pinecone Namespaces
To support thousands of independent Shopify stores, we use **Pinecone Namespaces**.
- **Isolation:** Each `store_id` maps to a unique `namespace`. 
- **Filtering:** All `upsert`, `fetch`, and `query` operations **must** pass the `namespace` parameter.
- **Dynamic Creation:** Pinecone creates namespaces on-the-fly when data is first upserted. No manual setup is required per store.

---

## 3. Mathematical Logic: The User Interest Vector
The core of the "For You" recommendation engine is the calculation of a **User Interest Vector** using weighted averaging in `app/services/recommender.py`.

### The Formula:
`UserVector = (V_purchased * W_p) + (V_cart * W_c) + (V_viewed * W_v)`

1.  **Fetch:** We fetch the high-dimensional vectors (1536d for OpenAI, 768d for Gemini) for every product in the user's history.
2.  **Category Averaging:** 
    *   `V_purchased`: Mean vector of all items the user bought.
    *   `V_cart`: Mean vector of all items added to the cart.
    *   `V_viewed`: Mean vector of all items viewed.
3.  **Weighting:** We apply weights from `app/core/config.py`:
    *   `WEIGHT_PURCHASED` (Default: 0.7)
    *   `WEIGHT_CART` (Default: 0.2)
    *   `WEIGHT_VIEWED` (Default: 0.1)
4.  **Normalization:** The final vector is normalized using L2-normalization to ensure compatibility with **Cosine Similarity** search in Pinecone.

---

## 4. AI Orchestration & Tracing
We use **LangChain** for embedding generation to allow for provider flexibility.

### Provider Switching
Controlled via `EMBEDDING_PROVIDER` in `.env`.
- `openai`: Uses `text-embedding-3-small`.
- `gemini`: Uses `models/gemini-embedding-001`.

### Observability (LangSmith)
The system is pre-configured for LangChain Tracing.
- **Automatic Detection:** `app/main.py` exports `LANGCHAIN_TRACING_V2=true` to the environment if enabled in `.env`.
- **Debugging:** All embedding calls are traced to LangSmith for monitoring performance and cost.

---

## 5. Detailed Data Flows

### A. Product Sync Flow
1.  **Input:** `Product` schema (title, tags, price, category, etc.).
2.  **Context Construction:** `format_product_context()` combines fields into a single semantic string (e.g., "Category: Shirts | Title: Blue Polo | Tags: casual, summer").
3.  **Embedding:** The string is sent to the configured provider (OpenAI/Gemini).
4.  **Storage:** The vector + metadata is upserted to Pinecone under the store's `namespace`.

### B. Personalized Recommendation Flow
1.  **Input:** `UserHistory` (Lists of IDs for purchased, cart, and viewed items) + `store_id`.
2.  **Vector Fetch:** `fetch_vectors` retrieves the actual vectors for those IDs from the store's namespace.
3.  **Profile Generation:** `calculate_user_vector` runs the weighted averaging logic.
4.  **Vector Search:** `query_nearest` finds the top_k items in the same namespace most similar to the user profile.
