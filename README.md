# Google ADK Agents

AI agents built using Google Agent Development Kit (ADK) and Gemini 2.0 Flash.

## Agents

### Single Tool Agent
A weather agent with one tool — fetches weather data for any city.

### Multi Tool Agent  
A versatile agent with three tools:
- Weather lookup
- Calculator (add, subtract, multiply, divide)
- Text summarizer

## Setup

```bash
pip install google-adk python-dotenv
```

Add your Gemini API key to `.env`:
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_key_here
```

## Run

```bash
python -m single_tool_agent.agent
python -m multi_tool_agent.agent
```
