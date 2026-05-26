"""Refund support agent with custom threshold approval middleware.

This graph demonstrates custom tool-call middleware with wrap_tool_call. The
middleware checks refund amounts and interrupts only when a refund is over $100.
In Studio, the middleware behavior appears inside the tool execution step rather
than as a separate graph node.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt


@tool
def lookup_order(order_id: str) -> str:
    """Look up a customer's order by ID."""
    orders = {
        "A100": "delivered, total $45.00",
        "B200": "delivered, total $120.00",
    }
    return orders.get(order_id, "order not found")


@tool
def issue_refund(order_id: str, amount: float, reason: str) -> str:
    """Issue a refund for a customer's order."""
    return f"Refund of ${amount:.2f} processed for order {order_id}. Reason: {reason}"


@wrap_tool_call
def refund_threshold_gate(request, handler):
    """Pause for human approval only when the refund amount exceeds $100."""
    if request.tool_call["name"] == "issue_refund":
        amount = request.tool_call["args"].get("amount", 0)

        print(f"\nMiddleware saw refund request for ${amount:.2f}")

        if amount > 100:
            print("Middleware paused execution for approval.")

            decision = interrupt(
                {
                    "action": "issue_refund",
                    "args": request.tool_call["args"],
                    "message": f"Refund of ${amount:.2f} exceeds the $100 threshold. Approve?",
                }
            )

            if not decision.get("approved", False):
                print("Middleware rejected the refund.")

                return ToolMessage(
                    content="Refund rejected by reviewer.",
                    tool_call_id=request.tool_call["id"],
                )

            print("Middleware approved the refund.")

    return handler(request)


agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[lookup_order, issue_refund],
    system_prompt=(
        "You are a customer refund support agent. "
        "Look up the order to get the total, then issue a refund for that amount."
    ),
    checkpointer=MemorySaver(),
    middleware=[refund_threshold_gate],
)
