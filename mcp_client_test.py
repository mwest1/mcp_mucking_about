from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
import asyncio
import logging

async def EvaluateExpression(session):
    expression = input("Enter a math expression (e.g., '5 * 7'): ")
    result = await session.call_tool(
        "EvaluateExpression",
        arguments={"expression": expression}
    )
    print("\n=== Calculation Result ===")
    print(f"Expression: {expression}")
    print(f"Result: {result}")
    print("==========================\n")

async def HourlyRate(session):
    JobList = ["Software Engineer", "Data Scientist", "Project Manager", "Designer"]
    print("#########################################################################")
    print("These are the available jobs: ")
    print("#########################################################################")
    print("| Number |   Position          |")
    print("|--------|---------------------|")
    for i, Job in enumerate(JobList, 1):
        print(f"|.   {str(i).ljust(10)}|{Job.ljust(20)}|")
    print("|--------|---------------------|")
    print("#########################################################################")

    try:
        JobNumber = int(input("Please enter the number of the job you want to know the hourly rate for: "))
        JobIndex = JobNumber - 1
        if JobIndex < 0 or JobIndex >= len(JobList):
            raise ValueError("Invalid job number")
        Job = JobList[JobIndex]
        result = await session.call_tool(
            "GetHourlyRate",
            arguments={"Job": Job}
        )
        print("\n=== Calculation Result ===")
        print(f"Position title: {Job}")
        print(f"Hourly Rate: {result}")
        print("==========================\n")
    except ValueError as e:
        print(f"Error: {e}")

# Dictionary mapping tool names to async functions
TOOL_FUNCTIONS = {
    "EvaluateExpression": EvaluateExpression,
    "GetHourlyRate": HourlyRate
}

async def run():
    level = logging.DEBUG
    async with streamablehttp_client("http://localhost:8888/mcp") as (read, write, *rest):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tool_list = (await session.list_tools()).tools

            # Display available tools
            print("#########################################################################")
            print("These are the available tools: ")
            print("#########################################################################")
            print("| Number | Tool Name           | Description                |")
            print("|--------|---------------------|----------------------------|")
            for i, tool in enumerate(tool_list, 1):
                print(f"|.   {str(i).ljust(4)} | {tool.name.ljust(19)} | {tool.description.ljust(26)} |")
            print("|--------|---------------------|----------------------------|")
            print("#########################################################################")

            try:
                FunctionChoice = int(input("Please enter the number of the tool you want to use: "))
                FunctionIndex = FunctionChoice - 1
                if FunctionIndex < 0 or FunctionIndex >= len(tool_list):
                    raise ValueError("Invalid tool number")
                
                functionName = tool_list[FunctionIndex].name
                print(f"You have chosen the tool: {functionName}")

                # Look up the function in the dictionary
                func = TOOL_FUNCTIONS.get(functionName)
                
                print(TOOL_FUNCTIONS)
                print(func)

                if func is None:
                    print(f"Error: No function mapped for tool '{functionName}'")
                    return
                
                print("Now calling the tool: ")
                await func(session)  # Await the async function

            except ValueError as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(run())


