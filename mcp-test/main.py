"""
FastMCP quickstart example.

Run:
    uv run server fastmcp_quickstart stdio
or start with:
    python server.py
"""

from mcp.server.fastmcp import FastMCP
from mcp.types import CreateMessageResult, ElicitResult, GetPromptResult
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()
port = int(os.environ.get("PORT", 10000))

# Create an MCP server
mcp = FastMCP("Demo")

# -------------------------------------------------
# 🧰 TOOLS
# -------------------------------------------------
@mcp.tool()
def greet(name: str = "World") -> CreateMessageResult:
    """Greet someone and return structured result"""
    message = f"Hello {name}!"
    result = CreateMessageResult(
        role="assistant",
        content={"type": "text", "text": message},
        model="demo-model"
    )
    print(result)
    print(isinstance(result, CreateMessageResult))
    return result


@mcp.tool()
def add(a: int, b: int) -> CreateMessageResult:
    """Add two numbers and return structured result"""
    result = a + b
    response = CreateMessageResult(
        role="assistant",
        content={"type": "text", "text": f"The sum of {a} and {b} is {result}."},
        model="demo-model"
    )
    print(response)
    print(isinstance(result, CreateMessageResult))
    return response



# -------------------------------------------------
# 🌐 RESOURCES
# -------------------------------------------------

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.resource("greeting://test")
def get_greeting_test() -> str:
    """Static greeting"""
    return f"Hello, test!"

@mcp.resource("employees://details")
def get_employee_details() -> dict:
    """Get a list of sample employee details"""
    employees = [
        {"id": 101, "name": "Alice Johnson", "role": "Software Engineer", "department": "Engineering", "email": "alice.johnson@example.com", "location": "New York"},
        {"id": 102, "name": "Bob Smith", "role": "QA Engineer", "department": "Quality Assurance", "email": "bob.smith@example.com", "location": "San Francisco"},
        {"id": 103, "name": "Charlie Brown", "role": "Product Manager", "department": "Product", "email": "charlie.brown@example.com", "location": "London"},
        {"id": 104, "name": "Diana Prince", "role": "DevOps Engineer", "department": "Infrastructure", "email": "diana.prince@example.com", "location": "Berlin"},
        {"id": 105, "name": "Ethan Hunt", "role": "Security Analyst", "department": "Cybersecurity", "email": "ethan.hunt@example.com", "location": "Singapore"},
        {"id": 106, "name": "Fiona Gallagher", "role": "Data Scientist", "department": "Data Analytics", "email": "fiona.gallagher@example.com", "location": "Toronto"},
        {"id": 107, "name": "George Miller", "role": "UI/UX Designer", "department": "Design", "email": "george.miller@example.com", "location": "Sydney"},
        {"id": 108, "name": "Hannah Lee", "role": "Frontend Developer", "department": "Engineering", "email": "hannah.lee@example.com", "location": "Tokyo"},
        {"id": 109, "name": "Ian Wright", "role": "Backend Developer", "department": "Engineering", "email": "ian.wright@example.com", "location": "Dublin"},
        {"id": 110, "name": "Julia Roberts", "role": "HR Manager", "department": "Human Resources", "email": "julia.roberts@example.com", "location": "Amsterdam"},
    ]
    return {"employees": employees}

# -------------------------------------------------
# 💬 PROMPTS
# -------------------------------------------------

@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> GetPromptResult:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    prompt_text = f"{styles.get(style, styles['friendly'])} for someone named {name}."
    
    return GetPromptResult(
        description="A prompt that asks for a specific style of greeting.",
        messages=[
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": prompt_text
                }
            }
        ],
        metadata={"style": style}
    )


# -------------------------------------------------
# 🧠 ELICIT EXAMPLE (dynamic result)
# -------------------------------------------------

@mcp.tool()
def elicit_feedback(question: str) -> ElicitResult:
    """Ask the user a follow-up question"""
    return ElicitResult(
        action={
            "name": "feedback",
            "description": "Ask for user feedback"
        },
        content={"type": "text", "text": f"Can you share your thoughts on: {question}? Or should I add 2+3 instead??"}
    )

@mcp.tool()
def elicit_feedback2(question: str) -> ElicitResult:
    """Ask the user a follow-up question"""
    return ElicitResult(
        action="accept",  # must be one of 'accept', 'decline', or 'cancel'
        content={
            "type": "text",
            "text": f"Can you share your thoughts on: {question}? Or should I add 2+3 instead?"
        }
    )

# -------------------------------------------------
# 🚀 MAIN ENTRY POINT
# -------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(mcp.streamable_http_app, host="0.0.0.0", port=port)