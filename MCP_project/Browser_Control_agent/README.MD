# 🌐 Browser Control Agent

A sophisticated AI-powered browser automation tool built with **MCP (Model Context Protocol)**, **Playwright**, and **Streamlit**. Control your browser using natural language instructions, powered by state-of-the-art LLMs like Google Gemini and OpenAI.

---

## ✨ Key Features

- **Natural Language Control**: Navigate, click, scroll, and type on any website by simply asking.
- **Visual Intelligence**: Automated screenshot capture and visual verification of web tasks.
- **Smart Summarization**: Extract and summarize content from complex web pages into clean Markdown.
- **MCP Integration**: Uses the Model Context Protocol to seamlessly interface with browser tools.
- **Elegant UI**: A premium Streamlit-powered dashboard for real-time interaction and feedback.

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10+
- Node.js (for Playwright MCP server)
- API Keys for Google Gemini or OpenAI

### 2. Installation

Clone the repository and install the dependencies:

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install streamlit mcp-agent playwright python-dotenv

# Install Playwright dependencies
playwright install chromium
```

### 3. Configuration

Create a `.env` file in the root directory:

```env
# Google Gemini (Default)
GOOGLE_API_KEY=your_google_api_key_here

# OpenAI (Optional)
OPENAI_API_KEY=your_openai_api_key_here
```

Ensure your `config.yaml` is set up to point to the Playwright MCP server:

```yaml
mcp:
  servers:
    playwright:
      command: "npx"
      args:
        - "-y"
        - "@playwright/mcp@latest"
```

---

## 🤖 Using OpenAI

To switch from Gemini to OpenAI, follow these steps:

1. **Update `agent.py`**:
   Replace `GoogleAugmentedLLM` with `OpenAIAugmentedLLM`.

   ```python
   # Import OpenAI Augmented LLM
   from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

   # In setup_agent method:
   # Change self.llm = await self.mcp_browser_agent.attach_llm(GoogleAugmentedLLM)
   # to:
   self.llm = await self.mcp_browser_agent.attach_llm(OpenAIAugmentedLLM)
   ```

2. **Add OpenAI Key**:
   Ensure `OPENAI_API_KEY` is present in your `.env` file.

---

## 🎮 Usage

Launch the interactive dashboard:

```bash
streamlit run agentui.py
```

### Example Commands:

- _"Navigate to github.com and find the latest trending repositories."_
- _"Go to news.ycombinator.com and summarize the top 3 stories."_
- _"Search for 'best mechanical keyboards' on Google and screenshot the first result."_

---

## 🛠 Tech Stack

- **[MCP-Agent](https://github.com/lastmile-ai/mcp-agent)**: Framework for building agentic workflows.
- **[Playwright](https://playwright.dev/)**: Reliable end-to-end testing for modern web apps.
- **[Streamlit](https://streamlit.io/)**: The fastest way to build and share data apps.
- **Google Gemini / OpenAI**: Advanced reasoning and language understanding.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

_Built with ❤️ for the AI community._
