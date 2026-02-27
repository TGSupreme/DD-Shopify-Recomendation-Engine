import asyncio
from app.services.embedding.gemini import GeminiProvider
from dotenv import load_dotenv

async def check():
    load_dotenv()
    try:
        provider = GeminiProvider()
        vector = await provider.embed_query("test")
        print(f"--- VERIFICATION ---")
        print(f"Model: {provider.client.model}")
        print(f"Actual Dimensions: {len(vector)}")
        print(f"--------------------")
    except Exception as e:
        print(f"Error checking dimensions: {e}")

if __name__ == "__main__":
    asyncio.run(check())
