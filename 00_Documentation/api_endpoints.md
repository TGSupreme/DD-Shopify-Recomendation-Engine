# API Endpoints Documentation

## Base URL
`http://localhost:8000/v1`

---

## 1. Sync Product (Single)
**Endpoint:** `POST /sync/`  
**Description:** Upserts a single product into the vector database within a store-specific namespace. Ideal for real-time Shopify webhooks.

**Request Body:**
```json
{
  "id": "p1",
  "store_id": "shopify-store-123",
  "title": "Premium Cotton Blue Shirt",
  "price": 45.0,
  "category": "Shirts",
  "availability": true,
  "tags": ["casual", "office"],
  "extra_metadata": {
    "material": "Cotton",
    "color": "Blue"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Product p1 synced successfully for store shopify-store-123",
  "upserted_count": 1
}
```

---

## 2. Bulk Sync Products
**Endpoint:** `POST /sync/bulk`  
**Description:** Upserts multiple products at once. Extremely efficient for the initial Shopify store import.

**Request Body:**
```json
{
  "store_id": "shopify-store-123",
  "products": [
    {
      "id": "p1",
      "store_id": "shopify-store-123",
      "title": "Blue Shirt",
      "price": 45.0
    },
    {
      "id": "p2",
      "store_id": "shopify-store-123",
      "title": "Red Pants",
      "price": 60.0
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Successfully synced 2 products for store shopify-store-123",
  "upserted_count": 2
}
```

---

## 3. Semantic Search
**Endpoint:** `POST /search/`  
**Description:** Searches for products within a specific store using natural language.

**Request Body:**
```json
{
  "query": "blue cotton shirt for office",
  "store_id": "shopify-store-123",
  "top_k": 10
}
```

**Response:**
```json
{
  "items": [
    { "product_id": "p1", "score": 0.92 },
    { "product_id": "p45", "score": 0.85 }
  ],
  "status": "success"
}
```

---

## 3. User Recommendations ("For You")
**Endpoint:** `POST /recommend/user`  
**Description:** Generates personalized recommendations based on a user's store-specific history.

**Request Body:**
```json
{
  "store_id": "shopify-store-123",
  "purchased": ["p1", "p2"],
  "add_to_cart": ["p10"],
  "viewed": ["p5", "p6", "p7"]
}
```

**Response:**
```json
{
  "items": [
    { "product_id": "p22", "score": 0.88 },
    { "product_id": "p99", "score": 0.81 }
  ],
  "status": "success"
}
```

---

## 4. Similar Products ("Related Items")
**Endpoint:** `POST /recommend/similar/{product_id}?store_id={store_id}`  
**Description:** Finds nearest neighbors for a specific product within the same store's namespace.

**Query Parameters:**
- `store_id` (Required): The ID of the Shopify store.

**Response:**
```json
{
  "items": [
    { "product_id": "p2", "score": 0.98 },
    { "product_id": "p3", "score": 0.95 }
  ],
  "status": "success"
}
```
