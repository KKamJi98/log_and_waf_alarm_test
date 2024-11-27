"""
Frontend에 대해 임의의 트래픽을 발생
"""

import random
import time
import aiohttp
import asyncio
from argparse import ArgumentParser

async def send_request(session, url):
    """비동기적으로 요청 전송"""
    try:
        async with session.get(url) as response:
            # 상태코드 확인
            # print(f"Request to {url} - Status: {response.status}")
            
            # CloudFront의 X-Cache 헤더 확인
            x_cache = response.headers.get("X-Cache", "Unknown")
            if x_cache == "Error from cloudfront":
                print(f"Request to {url} - Blocked (X-Cache: {x_cache})")
            else:
                print(f"Request to {url} - Allowed (X-Cache: {x_cache})")
    except aiohttp.ClientError as e:
        print(f"Error sending request to {url}: {e}")

async def generate_traffic(url, requests_per_interval, interval_seconds, duration_seconds):
    """지정된 URL로 요청을 초 단위로 전송"""
    total_intervals = duration_seconds // interval_seconds
    async with aiohttp.ClientSession() as session:
        for interval in range(total_intervals):
            print(f"Interval {interval + 1}: Sending {requests_per_interval} requests.")

            # 요청 전송
            tasks = [send_request(session, url) for _ in range(requests_per_interval)]
            await asyncio.gather(*tasks)

            # 초 단위 대기
            if interval < total_intervals - 1:  # 마지막 interval 이후에는 대기하지 않음
                print(f"Waiting for {interval_seconds} seconds before the next interval.")
                await asyncio.sleep(interval_seconds)

if __name__ == "__main__":
    parser = ArgumentParser(description="Generate traffic to a frontend.")
    parser.add_argument(
        "--url", type=str, default="https://rememberme.kkamji.net", help="Target URL"
    )
    parser.add_argument(
        "--requests_per_interval",
        type=int,
        required=True,
        help="Number of requests per interval",
    )
    parser.add_argument(
        "--interval_seconds", type=int, default=300, help="Interval duration in seconds"
    )
    parser.add_argument(
        "--duration_seconds", type=int, default=900, help="Total duration in seconds"
    )

    args = parser.parse_args()

    asyncio.run(
        generate_traffic(
            args.url, args.requests_per_interval, args.interval_seconds, args.duration_seconds
        )
    )