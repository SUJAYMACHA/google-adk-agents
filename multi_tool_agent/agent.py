import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()

def get_weather(city: str) -> dict:
    """Get mock weather data for a given city."""
    weather_data = {
        "hyderabad": {"temp": "32°C", "condition": "Sunny", "humidity": "45%"},
        "mumbai": {"temp": "29°C", "condition": "Humid", "humidity": "80%"},
        "delhi": {"temp": "35°C", "condition": "Hot", "humidity": "30%"},
    }
    city_lower = city.lower()
    if city_lower in weather_data:
        data = weather_data[city_lower]
        return {"status": "success", "city": city, **data}
    return {"status": "error", "message": f"No data for {city}"}

def calculator(operation: str, a: float, b: float) -> dict:
    """Perform basic math operations: add, subtract, multiply, divide."""
    ops = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else None
    }
    if operation not in ops:
        return {"status": "error", "message": "Invalid operation"}
    if operation == "divide" and b == 0:
        return {"status": "error", "message": "Cannot divide by zero"}
    return {"status": "success", "result": ops[operation]}

def summarize_text(text: str) -> dict:
    """Summarize a given block of text into key points."""
    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    summary = sentences[:2] if len(sentences) >= 2 else sentences
    return {
        "status": "success",
        "summary": ". ".join(summary) + ".",
        "original_length": len(text),
        "summary_length": len(". ".join(summary))
    }

multi_tool_agent = Agent(
    name="multi_tool_agent",
    model="gemini-2.0-flash",
    description="A versatile agent with weather, calculator, and text summarization tools.",
    instruction="""You are a smart multi-purpose assistant. You have three tools:
    1. get_weather - fetch weather for any city
    2. calculator - perform math operations (add, subtract, multiply, divide)
    3. summarize_text - summarize long text into key points
    Always pick the right tool based on what the user asks.""",
    tools=[get_weather, calculator, summarize_text],
)

APP_NAME = "multi_tool_app"
USER_ID = "user_01"
SESSION_ID = "session_01"

session_service = InMemorySessionService()
import asyncio
asyncio.run(session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID))

runner = Runner(agent=multi_tool_agent, app_name=APP_NAME, session_service=session_service)

def chat(user_input: str):
    message = types.Content(role="user", parts=[types.Part(text=user_input)])
    response_text = ""
    for event in runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response() and event.content and event.content.parts:
            response_text = event.content.parts[0].text
    return response_text

if __name__ == "__main__":
    print("Multi Tool Agent ready! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        response = chat(user_input)
        print(f"Agent: {response}\n")
