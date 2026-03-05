import asyncio
import numpy as np
from app.services.embedding import embed_query
from app.core.config import settings
from dotenv import load_dotenv

async def test_embedding_output():
    # Reload env to ensure we get the latest provider
    load_dotenv(override=True)
    
    test_text = "Popsicle Lip Balm - Disney Frozen Princess By RENEE, 2g"
    provider = settings.EMBEDDING_PROVIDER
    
    print(f"\n{'='*40}")
    print(f"EMBEDDING DIAGNOSTIC REPORT")
    print(f"{'='*40}")
    print(f"Active Provider: {provider.upper()}")
    print(f"Input Text:      '{test_text}'")
    
    try:
        vector = await embed_query(test_text)
        
        # Dimensions and Type
        dimensions = vector.shape[0]
        # Currently, all integrated providers (OpenAI, Gemini, Jina) return Dense vectors
        vector_type = "Dense" 
        
        print(f"Vector Type:     {vector_type}")
        print(f"Dimensions:      {dimensions}")
        print(f"Data Type:       {vector.dtype}")
        print(f"Sample (first 5): {vector[:5].tolist()}")
        
        # Quick validation
        if dimensions > 0:
            print(f"\nSUCCESS: Embedding generated successfully.")
        else:
            print(f"\nWARNING: Embedding has 0 dimensions.")
            
    except Exception as e:
        print(f"\nERROR: Failed to generate embedding.")
        print(f"Details: {str(e)}")
        print("\nNote: Ensure your API key is set in .env and the provider is correct.")
    
    print(f"{'='*40}\n")

if __name__ == "__main__":
    asyncio.run(test_embedding_output())
