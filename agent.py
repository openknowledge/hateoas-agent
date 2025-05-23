from agents import Agent, Runner, trace
import asyncio
from tools import delete_request, get_request, post_request, put_request
from prompts import system_prompt
import argparse

# Initialize the agent with the system prompt and tools
agent = Agent(
    name="HATEOAS Agent",
    instructions=system_prompt,
    tools=[get_request, post_request, delete_request, put_request],
)

# Define the command-line argument parser
def parse_args():
    parser = argparse.ArgumentParser(description="Run the HATEOAS agent.")
    parser.add_argument(
        "--prompt",
        type=str,
        help="The prompt for the agent.",
    )
    return parser.parse_args()


# Main function to run the agent with the provided prompt
async def main(prompt: str = None):
    with trace("HATEOAS Agent"):
        result = await Runner.run(agent, input=prompt)
    print(result.final_output)


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(prompt=args.prompt))