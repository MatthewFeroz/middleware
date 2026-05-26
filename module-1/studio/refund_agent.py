"""Basic refund support agent for LangGraph Studio.

This graph demonstrates the core agent loop without middleware. The agent looks
up an order, calls a refund tool, and returns a final customer-facing response.
Use this as the baseline trace before comparing the middleware examples.
"""

from langchain.agents import create_agent
from langchain_core.tools import tool


@tool
def lookup_order(order_id: str) -> str:
    """Look up a customer's order by ID."""
    orders = {
        "A100": "delivered, total $45.00",
        "B200": "delivered, total $120.00",
    }
    return orders.get(order_id, "order not found")


@tool
def issue_refund(order_id: str, reason: str) -> str:
    """Issue a refund for a customer's order."""
    return f"Refund processed for order {order_id}. Reason: {reason}"


agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[lookup_order, issue_refund],
    system_prompt="You are a customer refund support agent. Look up the order and issue a refund when a customer requests one.",
)
