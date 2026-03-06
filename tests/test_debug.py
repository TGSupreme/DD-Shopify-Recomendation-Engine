import httpx
import asyncio

async def test_debug_endpoint():
    url = "http://127.0.0.1:8000/v1/debug/"
    payload = {"test": "data", "message": "Hello from test script"}
    
    try:
        async with httpx.AsyncClient() as client:
            # Test POST
            response = await client.post(url, json=payload)
            print(f"POST Response: {response.status_code}")
            print(f"POST Content: {response.json()}")
            
            # Test GET
            response_get = await client.get(url, params={"key": "value"})
            print(f"GET Response: {response_get.status_code}")
            print(f"GET Content: {response_get.json()}")
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    asyncio.run(test_debug_endpoint())
