import asyncio
import aiohttp
import random
import time
from argparse import ArgumentParser


async def send_request(session, api_endpoint, path, method):
    """비동기적 요청 전송"""
    url = api_endpoint + path
    try:
        if method == "GET":
            async with session.get(url) as response:
                print(f"Request to {path} ({method}): Status Code {response.status}")
        elif method == "POST":
            async with session.post(url) as response:
                print(f"Request to {path} ({method}): Status Code {response.status}")
    except aiohttp.ClientError as e:
        print(f"Error during request to {path} ({method}): {e}")


async def send_requests(api_endpoint, duration_seconds):
    paths = {
        "/incorrectList": ["POST"],
        "/incorrectLists": ["GET"],
        "/incorrectWord": ["POST"],
        "/incorrectWords": ["POST"],
        "/list": ["POST"],
        "/lists": ["GET"],
        "/test": ["GET"],
        "/user": ["GET"],
        "/word": ["POST"],
        "/words": ["POST"],
    }

    start_time = time.time()
    count = 0
    async with aiohttp.ClientSession() as session:
        while time.time() - start_time < duration_seconds:
            count += 1
            path = random.choice(list(paths.keys()))
            method = random.choice(paths[path])

            # 비동기 요청 실행
            await send_request(session, api_endpoint, path, method)

            # 비동기 sleep (CPU 블로킹 방지)
            await asyncio.sleep(random.uniform(0.01, 0.05))

            elapsed = time.time() - start_time
            print(f"Elapsed time: {elapsed:.2f} seconds")
    print(f"traffic count => {count}")


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Generate traffic to an API Gateway connected Lambda functions."
    )
    parser.add_argument(
        "--api_endpoint",
        type=str,
        required=True,
        help="API Gateway Invoke URL (e.g. https://xxxxxx.execute-api.region.amazonaws.com/prod)",
    )
    parser.add_argument(
        "--duration_seconds",
        type=int,
        default=300,
        help="Total duration in seconds to generate traffic",
    )
    args = parser.parse_args()

    # asyncio.run을 사용하여 이벤트 루프 실행
    asyncio.run(send_requests(args.api_endpoint, args.duration_seconds))
