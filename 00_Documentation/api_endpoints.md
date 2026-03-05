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
  "id": "8034758590614",
  "store_id": "reneecosmetics.in",
  "title": "Popsicle Lip Balm - Disney Frozen Princess By RENEE, 2g",
  "product_type": "Lip Balm",
  "vendor": "Lips",
  "price": 299.0,
  "tags": [
    "disney",
    "Disney Frozen Princess By RENEE Popsicle Lip Balm",
    "Newly Launched",
    "princess by renee",
    "Princess by Renee products"
  ],
  "options": [
    {
      "name": "Color",
      "position": 1,
      "values": [
        "Anna",
        "Elsa"
      ]
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Product 8034758590614 synced successfully for store reneecosmetics.in",
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
  "store_id": "reneecosmetics.in",
  "products": [
    {
      "id": "p1",
      "store_id": "reneecosmetics.in",
      "title": "Blue Shirt",
      "product_type": "Shirts",
      "vendor": "ClassicWear",
      "price": 45.0,
      "tags": ["casual"],
      "options": []
    },
    {
      "id": "p2",
      "store_id": "reneecosmetics.in",
      "title": "Red Pants",
      "product_type": "Pants",
      "vendor": "DenimCo",
      "price": 60.0,
      "tags": ["formal"],
      "options": []
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Successfully synced 2 products for store reneecosmetics.in",
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
  "store_id": "reneecosmetics.in",
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

## 4. User Recommendations ("For You")
**Endpoint:** `POST /recommend/user`  
**Description:** Generates personalized recommendations based on a user's store-specific history.

**Request Body:**
```json
{
  "store_id": "reneecosmetics.in",
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

## 5. Similar Products ("Related Items")
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
