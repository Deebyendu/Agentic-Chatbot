# 🤖 Agentic Chatbot — LangGraph Stateful Agentic AI

A full-stack, end-to-end agentic AI application built with **LangGraph**, **Streamlit**, and support for multiple LLMs (Groq & Mistral). The app enables stateful, multi-node AI graph workflows across three use cases: a basic chatbot, a web-search-enabled chatbot, and an AI news aggregator.

---

## 📸 Preview

> Built with LangGraph state graphs, this app routes user interactions through dynamic AI nodes with conditional edges, tool integrations, and real-time Streamlit UI rendering.

---

## 🗂️ Project Structure

```
E2E AGENTIC CHATBOT/
├── AINews/                          # Output directory for generated news summaries
├── src/
│   └── langgraphagenticai/
│       ├── graph/
│       │   └── graph_builder.py     # Builds LangGraph state graphs per use case
│       ├── LLMS/
│       │   ├── groqllm.py           # Groq LLM initialization
│       │   └── mistralllm.py        # Mistral LLM initialization
│       ├── nodes/
│       │   ├── ai_news_node.py      # Fetch, summarize, and save AI news
│       │   ├── basic_chatbot_node.py        # Simple LLM chatbot node
│       │   └── chatbot_with_tool_node.py    # LLM chatbot with tool binding
│       ├── state/
│       │   └── state.py             # Shared LangGraph state definition
│       ├── tools/
│       │   └── search_tool.py       # Tavily web search tool integration
│       └── ui/
│           └── streamlitui/
│               ├── display_result.py    # Renders graph outputs in Streamlit
│               ├── loadui.py            # Loads sidebar UI and user controls
│               ├── uiconfigfile.ini     # UI configuration (models, titles, options)
│               └── uiconfigfile.py      # Config parser wrapper
│           └── main.py                  # App entry point logic
├── app.py                           # Top-level entry point
├── requirements.txt                 # Python dependencies
└── README.md
```

---

## 🚀 Features

- **Multi-LLM Support** — Switch between Groq and Mistral models from the sidebar without changing code.
- **Three Agentic Use Cases** — Each use case maps to a distinct LangGraph state graph:
  - 🗨️ **Basic Chatbot** — Stateful single-node chatbot using any configured LLM.
  - 🌐 **Chatbot with Web Search** — LLM enhanced with Tavily web search using conditional tool-routing edges.
  - 📰 **AI News** — A three-node pipeline (fetch → summarize → save) that retrieves and summarizes the latest AI news and writes it to a Markdown file.
- **LangGraph State Management** — All use cases use a typed `State` schema with LangGraph's `add_messages` annotation for message accumulation.
- **Streamlit UI** — Clean sidebar for LLM/model/use case selection and API key input, with inline chat and news rendering.
- **Config-Driven UI** — All labels, model lists, and use case options are driven by `uiconfigfile.ini` — no code changes needed to add new models.

---

## 🧠 How It Works

### State

All graphs share a common state schema defined in `state.py`:

```python
class State(TypedDict):
    messages: Annotated[List, add_messages]
```

This uses LangGraph's `add_messages` reducer to accumulate conversation history across graph nodes.

---

### Graph Architectures

#### 1. Basic Chatbot
```
START → chatbot → END
```
A single node that invokes the LLM directly on the current state messages.

#### 2. Chatbot with Web Search
```
START → chatbot ──(tool call?)──► tools
                ◄────────────────┘
        chatbot → END
```
The LLM is bound with Tavily search tools. LangGraph's built-in `tools_condition` routes to the tool node when the LLM emits a tool call, then routes back to the chatbot for a final response.

#### 3. AI News Pipeline
```
START → fetch_news → summarize_news → save_result → END
```
A sequential three-node pipeline:
- **`fetch_news`** — Calls the Tavily API to retrieve top AI news (daily/weekly/monthly).
- **`summarize_news`** — Passes fetched articles to the LLM with a structured prompt to produce a dated, markdown-formatted summary.
- **`save_result`** — Writes the summary to `./AINews/{frequency}_summary.md`.

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9+
- API keys for:
  - [Groq](https://console.groq.com/keys) and/or [Mistral](https://console.mistral.ai/)
  - [Tavily](https://app.tavily.com/home) (required for Chatbot with Web and AI News use cases)

### Installation

```bash
# Clone the repository
git clone https://github.com/Deebyendu/Agentic-Chatbot.git
cd e2e-agentic-chatbot

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

---

## 🔑 API Keys

API keys are entered securely via the Streamlit sidebar (password-masked inputs). They are never hardcoded. You will need:

| Key | Required For |
|---|---|
| `GROQ_API_KEY` | Basic Chatbot, Chatbot with Web (Groq models) |
| `MISTRAL_API_KEY` | Basic Chatbot, Chatbot with Web (Mistral models) |
| `TAVILY_API_KEY` | Chatbot with Web, AI News |

Optionally, you can set these as environment variables in a `.env` file:

```env
GROQ_API_KEY=your_groq_key
MISTRAL_API_KEY=your_mistral_key
TAVILY_API_KEY=your_tavily_key
```

---

## 🧩 Supported Models

Configured via `uiconfigfile.ini` — easily extensible.

**Groq:**
- `openai/gpt-oss-120b`
- `groq/compound`
- `qwen/qwen3-32b`

**Mistral:**
- `mistral-large-2512`
- `devstral-2512`
- `ministral-14b-latest`

---

## 📦 Dependencies

```
langchain
langchain_community
langchain_groq
langchain-mistralai
langchain-tavily
langchain-classic
langgraph
tavily
faiss-cpu
streamlit
python-dotenv
```

---

## 📁 AI News Output

When the **AI News** use case is run, a Markdown summary is saved to:

```
./AINews/daily_summary.md
./AINews/weekly_summary.md
./AINews/monthly_summary.md
```

The summary is formatted with dates (IST timezone), concise article summaries, and source URLs — sorted latest first.

---

## 🔧 Configuration

To add new models or use cases, edit `uiconfigfile.ini`:

```ini
[DEFAULT]
PAGE_TITLE = LangGraph: Build Stateful Agentic AI graph
LLM_OPTIONS = Groq, Mistral
USECASE_OPTIONS = Basic Chatbot, Chatbot with Web, AI News
GROQ_MODEL_OPTIONS = openai/gpt-oss-120b, groq/compound, qwen/qwen3-32b
MISTRAL_MODEL_OPTIONS = mistral-large-2512, devstral-2512, ministral-14b-latest
```

No other code changes are required to reflect new models in the UI.

---

## 🏗️ Extending the App

To add a new use case:

1. Create a new node file under `src/langgraphagenticai/nodes/`.
2. Register a new graph-building method in `graph_builder.py` and add it to `setup_graph()`.
3. Add display logic in `display_result.py` for the new use case.
4. Add the use case name to `USECASE_OPTIONS` in `uiconfigfile.ini`.

---

## 📄 License

This project is open source. See `LICENSE` for details.

---

## 🙌 Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph) — Stateful agentic graph framework
- [LangChain](https://github.com/langchain-ai/langchain) — LLM tooling and integrations
- [Tavily](https://tavily.com/) — AI-native web search API
- [Groq](https://groq.com/) — Ultra-fast LLM inference
- [Mistral AI](https://mistral.ai/) — Efficient open-weight LLMs
- [Streamlit](https://streamlit.io/) — Rapid Python UI framework
