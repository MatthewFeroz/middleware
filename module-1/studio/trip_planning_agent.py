"""Trip planning agent with todo list middleware.

This graph demonstrates TodoListMiddleware on a simple multi-step planning task.
The agent creates a todo list, checks weather, builds a packing list, suggests
an activity, and then returns a concise final plan.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get a simple weather forecast for a city."""
    forecasts = {
        "Seattle": "Cool and rainy, around 52°F. Bring a rain jacket.",
        "Austin": "Warm and sunny, around 78°F. Bring light clothing.",
        "New York": "Mild and breezy, around 60°F. Bring layers.",
    }

    return forecasts.get(city, f"No forecast found for {city}.")


@tool
def make_packing_list(city: str, days: int, trip_type: str) -> str:
    """Create a packing list for a trip."""
    return (
        f"Packing list for a {days}-day {trip_type} trip to {city}: "
        "rain jacket, comfortable shoes, laptop, charger, toiletries, "
        "two work outfits, casual evening clothes, and travel documents."
    )


@tool
def suggest_activity(city: str, time_of_day: str) -> str:
    """Suggest one activity for a city."""
    activities = {
        "Seattle": "Visit Pike Place Market and get dinner near the waterfront.",
        "Austin": "Walk around South Congress and listen to live music.",
        "New York": "Visit the High Line and grab dinner nearby.",
    }

    return activities.get(city, f"No activity suggestion found for {city}.")


agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather, make_packing_list, suggest_activity],
    system_prompt=(
        "You are a concise trip planning assistant. "
        "For every multi-step trip request, you must first use the todo list tool"
    ),
    middleware=[
        TodoListMiddleware(),
    ],
)
