from app.schemas.product import Product

def format_product_context(product: Product) -> str:
    """Format product attributes into a context string for embedding."""
    options_str = "; ".join([f"{opt.name}: {', '.join(opt.values)}" for opt in product.options])
    tags_str = ", ".join(product.tags)
    
    context = (
        f"Product: {product.title}. "
        f"Type: {product.product_type}. "
        f"Vendor: {product.vendor}. "
        f"Tags: {tags_str}. "
        f"Options: {options_str}."
    )
    return context
