import asyncio
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.agent.workflow import ReActAgent
from llama_index.llms.ollama import Ollama

# Initialize the MCP client
mcp_client = BasicMCPClient("http://localhost:8888/mcp")  # Point to your MCP server
mcp_tool_spec = McpToolSpec(client=mcp_client)

# Initialize Llama 3.1 via Ollama
llm = Ollama(model="llama3.2:1b", request_timeout=30.0)


# Get tools from the MCP server
async def get_tools():
    tools = await mcp_tool_spec.to_tool_list_async()
    return tools

# Create the LlamaIndex agent
async def create_agent():
    tools = await get_tools()
    agent = ReActAgent(
        tools=tools,
        llm=llm,
        system_prompt="You are an AI assistant that uses MCP tools to answer queries."
    )
    return agent

# Run the agent with a query
async def run_agent(query: str):
    agent = await create_agent()
    response = await agent.run(query)
    print(response)

# Example usage
if __name__ == "__main__":
    asyncio.run(run_agent("List the contents of the current directory"))