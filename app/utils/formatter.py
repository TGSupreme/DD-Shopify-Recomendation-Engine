from app.schemas.product import Product

def format_product_context(product: Product) -> str:
    """Format product attributes into a context string for embedding."""
    return f"Product: {product.title}. Color: {product.color}. Material: {product.material}. Tags: {','.join(product.tags)}"
