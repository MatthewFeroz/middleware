"""AI history research agent with summarization middleware.

This graph demonstrates SummarizationMiddleware with a short Wikipedia research
workflow. The agent gathers facts across multiple turns, summarizes older
context, and then synthesizes a final answer from the compressed history.
"""

import wikipedia

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


@tool
def fetch_wikipedia_summary(topic: str) -> str:
    """Fetch a short summary from Wikipedia for a topic."""
    try:
        page = wikipedia.page(topic, auto_suggest=False)
    except wikipedia.DisambiguationError as error:
        page = wikipedia.page(error.options[0], auto_suggest=False)
    except wikipedia.PageError:
        return f"No Wikipedia results found for {topic}."

    summary = wikipedia.summary(page.title, sentences=4, auto_suggest=False)
    return f"Title: {page.title}\nSource: {page.url}\n\n{summary}"


agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[fetch_wikipedia_summary],
    system_prompt=(
        "You are a concise research assistant. "
        "Use Wikipedia to gather facts across the conversation. "
        "When asked for a final answer, combine the important facts into a short, clear summary."
    ),
    checkpointer=InMemorySaver(),
    middleware=[
        SummarizationMiddleware(
            model="openai:gpt-4o-mini",
            trigger=("messages", 3),
            keep=("messages", 2),
        ),
    ],
)
