import os
import asyncio
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
        return {
            "status": "success",
            "city": city,
            "temperature": data["temp"],
            "condition": data["condition"],
            "humidity": data["humidity"]
        }
    return {"status": "error", "message": f"Weather data not found for {city}"}

weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    description="An agent that provides weather information for cities.",
    instruction="You are a helpful weather assistant. Use the get_weather tool to fetch weather data for any city the user asks about. Always present the information clearly.",
    tools=[get_weather],
)

APP_NAME = "weather_app"
USER_ID = "user_01"
SESSION_ID = "session_01"

session_service = InMemorySessionService()
asyncio.run(session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID))

runner = Runner(agent=weather_agent, app_name=APP_NAME, session_service=session_service)

def chat(user_input: str):
    message = types.Content(role="user", parts=[types.Part(text=user_input)])
    response_text = ""
    for event in runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response() and event.content and event.content.parts:
            response_text = event.content.parts[0].text
    return response_text

if __name__ == "__main__":
    print("Weather Agent ready! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        response = chat(user_input)
        print(f"Agent: {response}\n")
