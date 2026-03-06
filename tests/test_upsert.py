import asyncio
from app.schemas.product import Product, ProductOption
from app.services.embedding import embed_query
from app.services.vector_store import upsert_vector
from app.utils.formatter import format_product_context
from dotenv import load_dotenv

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

async def test_upsert():
    load_dotenv()
    
    # Define Demo Products using the new schema
    demo_products = [
        Product(
            id="p1", 
            store_id="test_store_1",
            title="Premium Cotton Blue Shirt", 
            product_type="Shirts",
            vendor="ClassicWear",
            tags=["casual", "office"], 
            price=45.0, 
            options=[
                ProductOption(name="Color", values=["Blue", "White"]),
                ProductOption(name="Size", values=["S", "M", "L"])
            ]
        ),
        Product(
            id="p2", 
            store_id="test_store_1",
            title="Slim Fit Black Jeans", 
            product_type="Pants",
            vendor="DenimCo",
            tags=["denim", "night-out"], 
            price=80.0, 
            options=[
                ProductOption(name="Color", values=["Black"]),
                ProductOption(name="Waist", values=["30", "32", "34"])
            ]
        ),
        Product(
            id="p3", 
            store_id="test_store_2",
            title="Woolen Winter Jacket", 
            product_type="Jackets",
            vendor="ArcticArmor",
            tags=["winter", "warm"], 
            price=120.0, 
            options=[
                ProductOption(name="Color", values=["Grey", "Navy"]),
                ProductOption(name="Material", values=["Wool"])
            ]
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
                "product_type": product.product_type,
                "vendor": product.vendor,
                "tags": product.tags,
                "options": [f"{opt.name}: {', '.join(opt.values)}" for opt in product.options]
            }
            
            # Upsert to Pinecone
            print(f"Upserting to Pinecone...")
            await upsert_vector(product.id, vector, metadata, namespace=product.store_id)
            logger.info(f"Successfully upserted product: {product.id} to store {product.store_id}")
            
        except Exception as e:
            print(f"Error upserting product {product.id}: {e}")

    print(f"--- UPSERT TEST COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(test_upsert())
