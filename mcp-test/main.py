"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()
port = int(os.environ.get("PORT" , 10000))

# Create an MCP server
mcp = FastMCP("Demo")


@mcp.tool()
def greet(name:str = "World") -> str:
    return f"Hello {name}"

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a dynamic greeting resource
@mcp.resource("greeting://test")
def get_greeting_test() -> str:
    """Get a personalized greeting"""
    return f"Hello, test!"


# Add an employee details resource with 10 sample records
@mcp.resource("employees://details")
def get_employee_details() -> dict:
    """Get a list of sample employee details"""
    employees = [
        {
            "id": 101,
            "name": "Alice Johnson",
            "role": "Software Engineer",
            "department": "Engineering",
            "email": "alice.johnson@example.com",
            "location": "New York"
        },
        {
            "id": 102,
            "name": "Bob Smith",
            "role": "QA Engineer",
            "department": "Quality Assurance",
            "email": "bob.smith@example.com",
            "location": "San Francisco"
        },
        {
            "id": 103,
            "name": "Charlie Brown",
            "role": "Product Manager",
            "department": "Product",
            "email": "charlie.brown@example.com",
            "location": "London"
        },
        {
            "id": 104,
            "name": "Diana Prince",
            "role": "DevOps Engineer",
            "department": "Infrastructure",
            "email": "diana.prince@example.com",
            "location": "Berlin"
        },
        {
            "id": 105,
            "name": "Ethan Hunt",
            "role": "Security Analyst",
            "department": "Cybersecurity",
            "email": "ethan.hunt@example.com",
            "location": "Singapore"
        },
        {
            "id": 106,
            "name": "Fiona Gallagher",
            "role": "Data Scientist",
            "department": "Data Analytics",
            "email": "fiona.gallagher@example.com",
            "location": "Toronto"
        },
        {
            "id": 107,
            "name": "George Miller",
            "role": "UI/UX Designer",
            "department": "Design",
            "email": "george.miller@example.com",
            "location": "Sydney"
        },
        {
            "id": 108,
            "name": "Hannah Lee",
            "role": "Frontend Developer",
            "department": "Engineering",
            "email": "hannah.lee@example.com",
            "location": "Tokyo"
        },
        {
            "id": 109,
            "name": "Ian Wright",
            "role": "Backend Developer",
            "department": "Engineering",
            "email": "ian.wright@example.com",
            "location": "Dublin"
        },        
        {
            "id": 110,
            "name": "Julia Roberts",
            "role": "HR Manager",
            "department": "Human Resources",
            "email": "julia.roberts@example.com",
            "location": "Amsterdam"
        }
    ]
    return {"employees": employees}



# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


if __name__ == "__main__":
    uvicorn.run(mcp.streamable_http_app, host="0.0.0.0", port=port)
