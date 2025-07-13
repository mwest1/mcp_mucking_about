from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
import asyncio
import logging

# Define server parameters to run the calculator server
server_params = StdioServerParameters(
    command="python",              # The executable to run
    args=["mcp_calculator.py"], # The server script (you’ll need to create this)
    env=None                       # Optional: environment variables (None uses defaults)
)

async def run():
    level = logging.debug
    # Start the server as a subprocess and get stdio read/write functions
    async with sse_client("http://localhost:8000/sse") as (read, write):
        # Create a client session to communicate with the server
        async with ClientSession(read, write) as session:
            # Initialize the connection to the server
            await session.initialize()

            # List available tools to confirm what’s there
            tools = await session.list_tools()
            tools = tools["tools"]
            print(tools)
            # print("\n=== Available Tools ===")
            # for tool in tools:
            #     print(f"- {tool}")
            # print("========================\n")

            # Get a math expression from the user
            expression = input("Enter a math expression (e.g., '5 * 7'): ")

            # Call the 'evaluate_expression' tool with the user’s input
            result = await session.call_tool(
                "evaluate_expression",
                arguments={"expression": expression}
            )
            print("\n=== Calculation Result ===")
            print(f"Expression: {expression}")
            print(f"Result: {result}")
            print("==========================\n")

if __name__ == "__main__":
    # Run the async function
    asyncio.run(run())