import asyncio
import numpy as np
from app.schemas.product import Product
from app.services.embedding import embed_query
from app.services.vector_store import upsert_vector
from app.utils.formatter import format_product_context
from dotenv import load_dotenv

async def test_upsert():
    load_dotenv()
    
    # 2. Define Demo Products
    demo_products = [
        Product(
            id="p1", 
            store_id="test_store_1",
            title="Premium Cotton Blue Shirt", 
            color="Blue", 
            material="Cotton", 
            tags=["casual", "office"], 
            price=45.0, 
            category="Shirts", 
            availability=True
        ),
        Product(
            id="p2", 
            store_id="test_store_1",
            title="Slim Fit Black Jeans", 
            color="Black", 
            material="Denim", 
            tags=["denim", "night-out"], 
            price=80.0, 
            category="Pants", 
            availability=True
        ),
        Product(
            id="p3", 
            store_id="test_store_2",
            title="Woolen Winter Jacket", 
            color="Grey", 
            material="Wool", 
            tags=["winter", "warm"], 
            price=120.0, 
            category="Jackets", 
            availability=True
        )
    ]

    print(f"--- UPSERT TEST START ---")
    
    for product in demo_products:
        try:
            # Format context string
            context = format_product_context(product)
            print(f"Embedding product: {product.id} - {product.title}...")
            
            # Generate embedding
            vector = await embed_query(context)
            
            # Prepare metadata
            metadata = {
                "title": product.title,
                "price": product.price,
                "category": product.category,
                "availability": product.availability
            }
            
            # Upsert to Pinecone
            print(f"Upserting to Pinecone...")
            await upsert_vector(product.id, vector, metadata, namespace=product.store_id)
            print(f"Successfully upserted product: {product.id} to store {product.store_id}")
            
        except Exception as e:
            print(f"Error upserting product {product.id}: {e}")

    print(f"--- UPSERT TEST COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(test_upsert())
