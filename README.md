![LangChain](assets/logo-light.svg)

# Introduction to Middleware

Welcome to LangChain Academy's Introduction to Middleware! This course introduces middleware in LangChain through a practical support-agent example, starting with the core agent loop and gradually moving toward more advanced middleware patterns.

## Python Version

Please use Python version 3.11, 3.12, or 3.13.

```bash
python3 --version
```

## Clone Repo

```bash
git clone https://github.com/MatthewFeroz/middleware
cd middleware
```

## Create an Environment and Install Dependencies

### Mac/Linux/WSL

```bash
python3 -m venv lc-academy-env
source lc-academy-env/bin/activate
pip install -r module-1/requirements.txt
```

### Windows PowerShell

```powershell
python3 -m venv lc-academy-env
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\lc-academy-env\Scripts\Activate.ps1
pip install -r module-1/requirements.txt
```

## Running Notebooks

If you don't have Jupyter set up, follow the installation instructions [here](https://jupyter.org/install).

Start Jupyter from the root of the repository:

```bash
jupyter notebook
```

## Sign Up for LangSmith

Create a [LangSmith](https://docs.langchain.com/langsmith/create-account-api-key) account and API key. You can reference the LangSmith docs [here](https://docs.smith.langchain.com/).

Then set the following values in your environment:

```bash
LANGSMITH_API_KEY="your-key"
LANGSMITH_TRACING=true
LANGSMITH_PROJECT="langchain-academy-middleware"
```

If you are on the EU instance, also set:

```bash
LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com
```

## Set Up OpenAI API Key

If you don't have an OpenAI API key, you can sign up [here](https://openai.com/index/openai-api/). OpenAI no longer has a free tier, so you may need to add funds to your OpenAI account.

Set your OpenAI API key in your environment:

```bash
OPENAI_API_KEY="your-key"
```

## Environment File

Module 1 includes an example environment file:

```text
module-1/.env.example
```

Copy it to `.env` before running the notebook or Studio examples:

```bash
cp module-1/.env.example module-1/.env
```

Then replace the placeholder values with your real API keys.

## Set Up LangGraph Studio

- LangGraph Studio is a custom IDE for viewing and testing agents.
- Studio can be run locally and opened in your browser on Mac, Windows, and Linux.
- See the documentation [here](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/#local-development-server).
- Studio assets for this course live in the `module-1/studio/` folder.

Install the Studio dependencies:

```bash
pip install -r module-1/studio/requirements.txt
```

To start the local development server, run the following command from the module's `studio` directory:

```bash
cd module-1/studio
langgraph dev
```

You should see output similar to:

```text
- API: http://127.0.0.1:2024
- Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- API Docs: http://127.0.0.1:2024/docs
```

Open your browser and navigate to the Studio UI:

```text
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

## References

- [LangChain Middleware Docs](https://docs.langchain.com/oss/python/langchain/middleware/overview)