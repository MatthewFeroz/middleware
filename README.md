![LangChain](assets/logo-light.svg)

# Middleware Explained

A short beginner lesson on middleware in LangChain.

The first module teaches middleware through a customer support desk analogy:

1. The core agent loop: model decides, tools run, results return to the model.
2. A tiny support agent that looks up order status.
3. A first middleware hook that observes tool calls with `@wrap_tool_call`.
4. Follow-up lesson ideas for approvals, error handling, prompt changes, and LangGraph composition.

Reference: https://docs.langchain.com/oss/python/langchain/middleware/overview
