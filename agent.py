from agents import Agent, Runner, function_tool, trace
import asyncio
import requests
import argparse
from pydantic import BaseModel


class HttpResponse(BaseModel):
    status_code: int
    body: dict | list | None  


def parse_args():
    parser = argparse.ArgumentParser(description="Run the HATEOAS agent.")
    parser.add_argument(
        "--prompt",
        type=str,
        help="The prompt for the agent.",
    )
    return parser.parse_args()


@function_tool
def get_request(url: str) -> HttpResponse:
    """
    Call a URL and return the status code and JSON response.
    """
    print(f"GET:{url}")
    response = requests.get(url)
    return HttpResponse(
        status_code=response.status_code,
        body=response.json()
    )


@function_tool(strict_mode=False)
def post_request(url: str, body: dict) -> HttpResponse:
    """
    Call a URL with a payload and return the status code and JSON response.
    """
    print(f"POST:{url}")
    response = requests.post(url, json=body)
    return HttpResponse(
        status_code=response.status_code,
        body=response.json()
    )


@function_tool
def delete_request(url: str) -> HttpResponse:
    """
    Call a URL and return the status code and JSON response (if any).
    """
    print(f"DELETE:{url}")
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
    """
    Call a URL with a payload and return the status code and JSON response.
    """
    print(f"PUT:{url}")
    response = requests.put(url, json=body)
    return HttpResponse(
        status_code=response.status_code,
        body=response.json()
    )


system_prompt = """
You are a HATEOAS agent.

Your role is to fulfill user requests by interacting with a HATEOAS-compatible REST API.

You do this by dynamically discovering and following hypermedia links provided in API responses, and by extracting request structure definitions using the `_templates` section when available.

You do not hardcode endpoint paths or assume the structure of the API in advance.
You rely entirely on what the server communicates through `_links`, `_templates`, and response metadata.

---

**Available tools (as defined):**
Each tool returns a `HttpResponse` object with the following structure:
```json
{
  "status_code": 200,
  "body": { ... }  // The full JSON response from the server
}

1. get_request(url: str) → HttpResponse
   - Sends a GET request and returns status_code + parsed JSON body.

2. post_request(url: str, body: dict) → HttpResponse
   - Sends a POST request with a JSON body. Returns status_code + parsed JSON body.

3. put_request(url: str, body: dict) → HttpResponse
   - Sends a PUT request with a JSON body. Returns status_code + parsed JSON body.

4. delete_request(url: str) → HttpResponse
   - Sends a DELETE request. Returns status_code + parsed JSON body (or null if none).

---

**Your job is to navigate the API hypermedia-style:**

- Start from the known entry point: `http://localhost:8080/`.
- Use `get_request()` to retrieve resources and inspect the `body` for `_links` and `_templates`.
- Only perform actions explicitly allowed and defined in `_links` (e.g. `self`, `next`, `delete`, `update`, `create`).
- Use `_templates` to determine the expected structure of request bodies for POST and PUT actions.
- Construct request bodies strictly based on the fields defined in `_templates`.
- Only perform POST, PUT, or DELETE if `_links` explicitly includes the corresponding method and target.

---

**Rules:**

- Never guess or invent URLs, methods, or data structures.
- Always use `_links` to determine what actions are allowed.
- Only send POST or PUT requests if a matching `_template` is available.
- Use DELETE only when `_links` explicitly includes a relation for it.
- Every response includes a `status_code` you must check to confirm success (e.g. 200, 201, 204).
- Parse the `body` field to read `_links`, `_templates`, and resource content.
- Always describe your reasoning step-by-step before choosing the next action.

---

**Templates:**

If a response includes `_templates`, it defines the expected structure for request bodies.

Example:
```json
"_templates": {
  "default": {
    "method": "PUT",
    "properties": [
      { "name": "title", "type": "text", "required": true },
      { "name": "description", "type": "text", "required": false }
    ]
  }
}
"""

agent = Agent(
    name="HATEOAS Agent",
    instructions=system_prompt,
    tools=[get_request, post_request, delete_request, put_request],
)

async def main(prompt: str = None):
    with trace("HATEOAS Agent"):
        result = await Runner.run(agent, input=prompt)
    print(result.final_output)



if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(prompt=args.prompt))