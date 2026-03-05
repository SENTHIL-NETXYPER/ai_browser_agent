# AI Browser Agent

An AI agent that uses an LLM to decide actions and controls the browser—Google search or open a URL.

## Setup

1. **Clone and enter the project**
   ```bash
   git clone https://github.com/SENTHIL-NETXYPER/ai_browser_agent.git
   cd ai_browser_agent
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

4. **Set your OpenAI API key**
   - **PowerShell:** `$env:OPENAI_API_KEY = "your-key-here"`
   - **Cmd:** `set OPENAI_API_KEY=your-key-here`
   - Or use a `.env` file (add `python-dotenv` and load it in code).

## Run

```bash
python main.py
```

Enter an instruction (e.g. "search for Python tutorials" or "open https://example.com"). The agent will choose `google_search` or `open_website` and run it.

## Project structure

- `main.py` — Entry point; reads user input and runs the agent loop.
- `llm_service.py` — Calls OpenAI to decide which tool and parameters to use.
- `tool_router.py` — Dispatches to the right tool from the LLM decision.
- `browser.py` — Playwright-based Google search and open-website actions.

## Requirements

- Python 3.9+
- OpenAI API key
- Playwright (Chromium is installed via `playwright install`)
