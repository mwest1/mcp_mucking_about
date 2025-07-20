from mcp.server.fastmcp import FastMCP
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

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
@server.tool(name="Get the weather", description="Get the weather for a given location. Uses a string as input, which must be converted to lattitude and longitude.")
def GetWeather(location: str) -> str:
    """Returns the weather for a given location. User input is the name of the city, which is converted to latitude and longitude."""
    url = "https://api.open-meteo.com/v1/forecast"
    try:
    # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)
        # Get the latitude and longitude for the location
        location = location.strip()
        lat, lon = openmeteo.geocode(location)
        # Construct the params for the weather request 
        params = {
            "latitude": lat,
            "longitude": lon,
	        "daily": ["daylight_duration", "sunshine_duration"],
	        "models": "bom_access_global",
	        "timezone": "auto",
	        "forecast_days": 3
        }
        responses = openmeteo.weather_api(url, params=params)
        print(responses)

    except Exception as e:
        raise ValueError(f"Could not find location: {e}")

# Run the server over sse
if __name__ == "__main__":
    server.run(transport="streamable-http")