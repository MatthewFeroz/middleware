"""AI history research agent with summarization middleware.

This graph demonstrates SummarizationMiddleware with a short Wikipedia research
workflow. The agent gathers facts across multiple turns, summarizes older
context, and then synthesizes a final answer from the compressed history.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.tools import tool


retriever = WikipediaRetriever(
    top_k_results=1,
    doc_content_chars_max=8_000,
)


@tool
def fetch_wikipedia_data(query: str) -> str:
    """Fetch content of the Wikipedia page from the top hit for a query."""
    results = retriever.invoke(query)
    if results:
        return results[0].page_content
    return "(No data found)"


summary_prompt = """
Summarize the main thrust of this conversation. What have the human and assistant
discussed so far? Focus on key facts and requests.
<messages>
Messages to summarize:
{messages}
</messages>
"""


agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[fetch_wikipedia_data],
    system_prompt=(
        "You are a concise research assistant. "
        "Use Wikipedia to gather facts across the conversation. "
        "When asked for a final answer, combine the important facts into a short, clear summary."
    ),
    middleware=[
        SummarizationMiddleware(
            model="openai:gpt-4o-mini",
            summary_prompt=summary_prompt,
            trigger=("fraction", 0.7),
            keep=("fraction", 0.3),
            trim_tokens_to_summarize=None,
        ),
    ],
)
