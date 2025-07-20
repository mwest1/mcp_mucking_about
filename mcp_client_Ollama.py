import asyncio
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.agent.workflow import ReActAgent
from llama_index.llms.ollama import Ollama

# Initialize the MCP client
mcp_client = BasicMCPClient("http://localhost:8888/mcp")  # Point to your MCP server
mcp_tool_spec = McpToolSpec(client=mcp_client)
llm_model = "llama3.1:latest"  # Specify the LLM model to use
# Initialize Llama 3.1 via Ollama
llm = Ollama(model=llm_model, request_timeout=120.0, base_url="http://127.0.0.1:11434")


# Get tools from the MCP server
async def get_tools():
    tools = await mcp_tool_spec.to_tool_list_async()
    #print(f"Available tools: {tools}")
    return tools

# Create the LlamaIndex agent
async def create_agent():
    tools = await get_tools()
    agent = ReActAgent(
        tools=tools,
        llm=llm,
        system_prompt="""You are an AI assistant that uses MCP tools to answer queries. Use the tools provided to assist with the users queries.
        If you need to evaluate a mathematical expression, use the EvaluateExpression tool. If you need to find the hourly rate for a job, use the HourlyRate tool.
        Always provied a clear and concise response to the user's query.  
        """
    )
    #print(agent)
    return agent

# Run the agent with a query
async def run_agent(query: str):
    agent = await create_agent()
    response = await agent.run(query)
    print(response)

# Example usage
if __name__ == "__main__":
    prompt = input("What is your task for the LLM, {}?".format(llm_model))
    asyncio.run(run_agent(prompt))