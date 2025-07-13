from mcp.server.fastmcp import FastMCP

# Create the server. This Server will run on the local host on port 8000. 

server = FastMCP("My Calculator Server", host="localhost", port=8888,json_response=True, stateless_http=True)
# Define the calculator tool
@server.tool(name="EvaluateExpression", description="Evaluates a mathematical expression and returns the result")
def EvaluateExpression(expression: str) -> float:
    """Evaluates a mathematical expression and returns the result."""
    try:
        # Warning: eval() is unsafe for untrusted input; use a proper parser in production
        result = eval(expression, {"__builtins__": {}}, {"sum": sum})
        return result
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")
@server.tool(name="HourlyRate", description="Tells the hourly rate of a job")
def  HourlyRate(job: str) -> float:
    """Returns the hourly rate for a given job."""
    hourly_rates = {
        "Software Engineer": 50.0,
        "Data Scientist": 60.0,
        "Project Manager": 55.0,
        "Designer": 45.0
    }
    return hourly_rates.get(job, 40.0)

# Run the server over sse
if __name__ == "__main__":
    server.run(transport="streamable-http")