import asyncio
import aiohttp
import random
import time

URL = "https://cloud-nulp-333675083625.europe-west1.run.app/users"

CONCURRENT_CLIENTS = 30

REQUESTS_PER_CLIENT = 40

async def send_request(session, client_id, request_id):
    try:
        async with session.get(URL) as resp:
            status = resp.status
            print(f"[Client {client_id} Req {request_id}] Status: {status}")
    except Exception as e:
        print(f"[Client {client_id} Req {request_id}] Error: {e}")

async def client_simulator(client_id):
    async with aiohttp.ClientSession() as session:
        for i in range(REQUESTS_PER_CLIENT):
            await send_request(session, client_id, i)
            await asyncio.sleep(random.uniform(0.05, 0.5))

async def main():
    tasks = [client_simulator(i) for i in range(CONCURRENT_CLIENTS)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(f"Completed in {time.time() - start:.2f} seconds")
