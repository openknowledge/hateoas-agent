from agents import function_tool
import requests
from pydantic import BaseModel
import logging

# Set root logger to WARNING (suppresses most library logs)
logging.basicConfig(level=logging.WARNING)

# Configure your logger to INFO
logger = logging.getLogger("hateoas.tools")
logger.setLevel(logging.INFO)

class HttpResponse(BaseModel):
    status_code: int
    body: dict | list | None

@function_tool
def get_request(url: str) -> HttpResponse:
    logger.info(f"GET: {url}")
    response = requests.get(url)
    return HttpResponse(
        status_code=response.status_code,
        body=response.json()
    )

@function_tool(strict_mode=False)
def post_request(url: str, body: dict) -> HttpResponse:
    logger.info(f"POST: {url}")
    response = requests.post(url, json=body)
    return HttpResponse(
        status_code=response.status_code,
        body=response.json()
    )

@function_tool
def delete_request(url: str) -> HttpResponse:
    logger.info(f"DELETE: {url}")
    response = requests.delete(url)
    try:
        json_body = response.json()
    except ValueError:
        json_body = None
    return HttpResponse(
        status_code=response.status_code,
        body=json_body
    )

@function_tool(strict_mode=False)
def put_request(url: str, body: dict) -> HttpResponse:
    logger.info(f"PUT: {url}")
    response = requests.put(url, json=body)
    return HttpResponse(
        status_code=response.status_code,
        body=response.json()
    )