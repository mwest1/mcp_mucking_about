from mcp.server.fastmcp import FastMCP

# Create the server. This Server will run on the local host on port 8000. 
# 
server = FastMCP("My Calculator Server", host="localhost", port=8000)

# Define the calculator tool
@server.tool(name="evaluate_expression", description="Evaluates a mathematical expression and returns the result")
def evaluate_expression(expression: str) -> float:
    """Evaluates a mathematical expression and returns the result."""
    try:
        # Warning: eval() is unsafe for untrusted input; use a proper parser in production
        result = eval(expression, {"__builtins__": {}}, {"sum": sum})
        return result
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

# Run the server over sse
if __name__ == "__main__":
    server.run(transport="sse")