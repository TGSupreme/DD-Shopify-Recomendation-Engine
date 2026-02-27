# Recommendation Engine: System Architecture & Design

## 1. Project Overview
A high-performance, **stateless** recommendation service built with **FastAPI**. This module acts as the AI intelligence layer for the Shopify-To-Mongo ecosystem. It transforms raw product data into vector embeddings and calculates user preferences based on their shopping behavior.

---

## 2. Core Technical Stack
*   **Framework:** FastAPI (Python)
*   **Vector Database:** Pinecone
*   **AI Orchestration:** LangChain (for pluggable embedding models)
*   **Mathematical Operations:** NumPy (for high-speed vector weighted averaging)
*   **Embedding Models:** OpenAI (`text-embedding-3-small` - 1536 dims) and Google Gemini (`gemini-embedding-001` - 3072 dims)
*   **External Integration:** Communicates with an Express.js server (primary data source)

---

## 3. System Architecture
The system follows a **stateless architecture**, meaning it does not maintain a local database. All persistent state is stored in **Pinecone** (vectors) and **MongoDB** (managed by the separate Express server).

### Data Flow Path:
1.  **Express Server:** Sends product or user behavior JSON to FastAPI.
2.  **FastAPI (Vectorizer):** Processes JSON, formats content strings, and generates embeddings via LangChain.
3.  **FastAPI (Processor):** Fetches existing vectors from Pinecone and performs weighted averaging.
4.  **Pinecone:** Performs "Nearest Neighbor" (ANN) search to find similar products.
5.  **FastAPI (Response):** Returns a list of Product IDs and similarity scores to Express.

---

## 4. API Endpoints (FastAPI)

### `POST /sync`
*   **Purpose:** Keep Pinecone in sync with Shopify/MongoDB.
*   **Input:** Entire Product JSON from Express.
*   **Logic:** 
    *   Construct a context string: `f"Product: {title}. Color: {color}. Material: {material}. Tags: {tags}"`.
    *   Generate vector via LangChain.
    *   Upsert to Pinecone with Metadata (`price`, `category`, `availability`, `gender`).

### `POST /recommend/user`
*   **Purpose:** Generate "For You" personalized recommendations.
*   **Input:** User history JSON containing three objects: `purchased`, `add_to_cart` (or `liked`), and `viewed`.
*   **Logic:**
    1.  Extract all Product IDs from history.
    2.  Fetch vectors for these IDs from Pinecone (using `index.fetch`).
    3.  **Fallback:** If a product is missing from Pinecone, embed its "Entire Data" on-the-fly using LangChain.
    4.  **Weighted Average Calculation:**
        *   `V_purchased = Average(purchased_vectors) * 0.7`
        *   `V_cart = Average(cart_vectors) * 0.2`
        *   `V_viewed = Average(viewed_vectors) * 0.1`
        *   `User_Vector = Normalize(V_purchased + V_cart + V_viewed)`
    5.  Query Pinecone with `User_Vector` to get Top N results.

### `POST /recommend/similar`
*   **Purpose:** "Related Items" for a product page.
*   **Input:** Product ID or raw Product JSON.
*   **Logic:** Find the nearest neighbors in Pinecone based on the product's vector.

### `POST /search`
*   **Purpose:** Semantic search (natural language).
*   **Input:** Search string (e.g., "warm winter jacket for skiing").
*   **Logic:** Embed the string using LangChain and query Pinecone.

---

## 5. Vectorization Strategy
To ensure maximum flexibility, the system uses the **LangChain Embedding Interface**. This allows switching between models without rewriting the core logic.

*   **Content String Formatting:** Consistent mapping of JSON fields into a text block before embedding.
*   **Normalization:** All vectors are normalized to unit length for optimal **Cosine Similarity** performance in Pinecone.

---

## 6. Key Design Decisions
*   **Statelessness:** Enables horizontal scaling. No local database or session storage required.
*   **Weighted Preferences:** Prioritizes actual purchases over casual views to ensure relevant recommendations.
*   **Metadata Filtering:** Supports complex queries (e.g., "Find similar products under $100") directly in the vector search.
*   **Cold Start Handling:** On-the-fly embedding for new products that haven't been indexed yet.

---

## 7. Environment Configuration
Required variables for the module:
*   `EMBEDDING_PROVIDER`: (openai | gemini)
*   `OPENAI_API_KEY`
*   `GOOGLE_API_KEY`
*   `PINECONE_API_KEY`
*   `PINECONE_INDEX_NAME`
*   `WEIGHT_PURCHASED`: (Default: 0.7)
*   `WEIGHT_CART`: (Default: 0.2)
*   `WEIGHT_VIEWED`: (Default: 0.1)
