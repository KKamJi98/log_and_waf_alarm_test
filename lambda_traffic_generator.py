"""
API Gateway와 연결된 lambda 함수들에 대해 임의의 트래픽 발생
"""

import asyncio
import aiohttp
import boto3
import random
import time


def get_parameter(parameter_name):
    ssm = boto3.client("ssm", region_name="ap-northeast-2")

    try:
        response = ssm.get_parameter(Name=parameter_name)
        return response["Parameter"]["Value"]
    except ssm.exceptions.ParameterNotFound:
        print(f"Parameter '{parameter_name}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


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
            await asyncio.sleep(random.uniform(1, 2))

            print(f"Elapsed time: {time.time() - start_time:.2f} seconds")
    print(f"traffic count => {count}")


if __name__ == "__main__":
    parameter_name = "/remember-me/api_gateway_endpoint_invoke_url"
    api_gateway_endpoint_invoke_url = get_parameter(parameter_name)

    if api_gateway_endpoint_invoke_url:
        # asyncio.run을 사용하여 이벤트 루프 실행
        asyncio.run(
            send_requests(api_gateway_endpoint_invoke_url, duration_seconds=3600)
        )  # 1시간
    else:
        print("Failed to retrieve the API Gateway endpoint URL.")
