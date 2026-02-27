# import asyncio
# from app.api.deps import get_embedding_provider

# async def test_embedding():
#     """Simple test to verify embedding generation."""
#     try:
#         embedding_provider = get_embedding_provider()
#         text = "Hello how are you"
        
#         print(f"Generating embedding for: '{text}'...")
#         vector = await embedding_provider.embed_query(text)
        
#         print(f"Vector generated successfully!")
#         print(f"Vector dimensions: {len(vector)}")
#         print(f"First 5 values: {vector[:5]}")
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     asyncio.run(test_embedding())

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vector = embeddings.embed_query("hello, world!")
print(len(vector))