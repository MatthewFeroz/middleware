"""Refund support agent with built-in human-in-the-loop middleware.

This graph uses LangChain's HumanInTheLoopMiddleware to pause before the refund
tool runs. In LangGraph Studio, the interrupt can be approved, edited, or
rejected so learners can inspect how tool approval changes the trace.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
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
def issue_refund(order_id: str, amount: float = 45.0, reason: str = "Customer requested refund") -> str:
    """Issue a refund for a customer's order."""
    return f"Refund of ${amount:.2f} processed for order {order_id}. Reason: {reason}"


agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[lookup_order, issue_refund],
    system_prompt=(
        "You are a customer refund support agent. "
        "Look up the order and issue a refund when a customer requests one."
    ),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "issue_refund": {"allowed_decisions": ["approve", "edit", "reject"]},
            }
        )
    ],
)
