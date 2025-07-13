from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
import asyncio
import logging


async def EvaluateExpression(session):
    # Get a math expression from the user
    expression = input("Enter a math expression (e.g., '5 * 7'): ")

    # Call the 'evaluate_expression' tool with the user’s input
    result = await session.call_tool(
        "EvaluateExpression",
        arguments={"expression": expression}
    )
    print("\n=== Calculation Result ===")
    print(f"Expression: {expression}")
    print(f"Result: {result}")
    print("==========================\n")

async def HourlyRate(session):
    # Define a "Database" of the available jobs
    JobList = ["Software Engineer", "Data Scientist", "Project Manager", "Designer"]
    # Get the user to input a Job from the list 
    print("#########################################################################") 
    print("These are the available jobs: ")
    print("#########################################################################")
    print("| Number |   Position          |")
    print("|--------|---------------------|") 
    i=0
    for Job in JobList:
        print("|.   "+str(i+1).ljust(10)+"|{}".format(Job.ljust(20)) + "|")
        i = i + 1

    print("|--------|---------------------|") 
    print("#########################################################################")

    JobNumber = int(input("Please enter the number of the job you want to know the hourly rate for: "))
    JobIndex = JobNumber - 1
    Job = JobList[JobIndex] 
    # Call the 'evaluate_expression' tool with the user’s input
    result = await session.call_tool(
        "HourlyRate",
        arguments={"job": Job} 
    )
    print("\n=== Calculation Result ===")
    print(f"Position title: {Job}")
    print(f"Hourly Rate: {result}")
    print("==========================\n")



# create an empty dictionary to hold the tool functions
TOOL_FUNCTIONS = {
    "EvaluateExpression": EvaluateExpression,
    "HourlyRate": HourlyRate
}
async def run():
    level = logging.DEBUG
    # Start the server as a subprocess and get stdio read/write functions
    async with streamablehttp_client("http://localhost:8888/mcp") as (read, write, *rest):
        # Create a client session to communicate with the server
        async with ClientSession(read, write) as session:
            # Initialize the connection to the server
            await session.initialize()

            # List available tools to confirm what’s there
            tool_list = await session.list_tools()
            tool_list = tool_list.tools
            i = 0
            print("#########################################################################") 
            print("These are the available tools: ")
            print("#########################################################################")
            print("| Number | Tool Name           |.           Description ")
            print("|--------------------|--------------------|") 
            while i < len(tool_list):
                print("|.   "+str(i+1).ljust(10)+"{}".format(tool_list[i].name).ljust(20) + "|" + "{}".format(tool_list[i].description).ljust(20) + "|")
                i = i + 1
            print("|--------------------|--------------------|")
            print("#########################################################################")
            
            # add the tool functions to the Dictionary 
            #TOOL_FUNCTIONS = {tool.name.replace(" ", ""): tool.name.replace(" ", "") for tool in tool_list}
            print(TOOL_FUNCTIONS)
            FunctionChoice = int(input("Please enter the number the tool you want to use: "))
            FunctionIndex = FunctionChoice - 1
            functionName = tool_list[FunctionIndex].name
            print("You have chosen the tool: " + functionName)
            
            print("Now calling the tool: ")
            functionName = TOOL_FUNCTIONS[functionName]
            print(functionName)
            await functionName(session)




if __name__ == "__main__":
    # Run the async function
    asyncio.run(run())