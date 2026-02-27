# Recommendation Engine: API Endpoints Documentation

This document provides a detailed technical reference for the FastAPI Recommendation Service. All endpoints are versioned under `/v1`.

---

## 1. Product Synchronization

### `POST /v1/sync/`
**Purpose:** Keeps the Pinecone vector database in sync with the primary Shopify/MongoDB product data.

**Request Body (`Product` Schema):**
```json
{
  "id": "prod_123",
  "title": "Classic Cotton T-Shirt",
  "color": "Blue",
  "material": "100% Cotton",
  "tags": ["casual", "summer", "basics"],
  "price": 29.99,
  "category": "Apparel",
  "availability": true,
  "gender": "Unisex",
  "extra_metadata": {
    "brand": "EcoWear",
    "sku": "TSH-B-001"
  }
}
```

**Logic:**
1. Formats attributes into a context string: `Product: Classic Cotton T-Shirt. Color: Blue. Material: 100% Cotton. Tags: casual,summer,basics`.
2. Generates a vector embedding using the configured provider (OpenAI or Gemini).
3. Upserts the vector to Pinecone with the provided metadata for filtering.

**Response (`SyncResponse`):**
```json
{
  "status": "success",
  "message": "Product prod_123 synced successfully",
  "upserted_count": 1
}
```

---

## 2. Personalized Recommendations

### `POST /v1/recommend/user`
**Purpose:** Generates a "For You" list of recommended products based on a user's interaction history.

**Request Body (`UserHistory` Schema):**
```json
{
  "purchased": ["id_1", "id_2"],
  "add_to_cart": ["id_3"],
  "viewed": ["id_4", "id_5", "id_6"]
}
```

**Logic:**
1. Fetches existing vectors for all provided IDs from Pinecone.
2. Calculates a **User Interest Vector** using weighted averaging:
   - **Purchased:** 70% weight
   - **Cart/Liked:** 20% weight
   - **Viewed:** 10% weight
3. Normalizes the resulting vector.
4. Queries Pinecone for the Top 10 nearest neighbors.

**Response (`RecommendationResponse`):**
```json
{
  "items": [
    { "product_id": "prod_789", "score": 0.982 },
    { "product_id": "prod_456", "score": 0.945 }
  ],
  "status": "success"
}
```

---

## 3. Related Items

### `POST /v1/recommend/similar/{product_id}`
**Purpose:** Finds products similar to a specific item (used for "Related Products" sections).

**Path Parameter:**
- `product_id` (string): The ID of the product to find similarities for.

**Logic:**
1. Fetches the vector for the given `product_id`.
2. Performs a nearest neighbor search in Pinecone using that vector.

**Response (`RecommendationResponse`):**
```json
{
  "items": [
    { "product_id": "prod_related_1", "score": 0.991 },
    { "product_id": "prod_related_2", "score": 0.885 }
  ],
  "status": "success"
}
```

---

## 4. Semantic Search

### `POST /v1/search/`
**Purpose:** Enables natural language search (e.g., "Find me a warm jacket for a winter trip").

**Query Parameter:**
- `query` (string): The natural language search string.

**Logic:**
1. Generates an embedding for the search string.
2. Queries Pinecone for the Top 10 most semantically similar products.

**Response (`RecommendationResponse`):**
```json
{
  "items": [
    { "product_id": "winter_jacket_01", "score": 0.921 },
    { "product_id": "parka_blue", "score": 0.895 }
  ],
  "status": "success"
}
```

---

## Error Handling
In case of an error (e.g., missing API keys, database connection issues), the API returns a `500 Internal Server Error` with a detailed message:
```json
{
  "detail": "Error message description here"
}
```
