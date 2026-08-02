# SpendSnap — AI-Powered Telegram Expense Tracker Bot
---

## Executive Summary

**SpendSnap** (`@SpendSnap_kushagra_bot`) is an intelligent, agentic Telegram bot designed for automated personal expense tracking and financial analysis. Powered by **LangGraph** stateful workflows, **LangChain**, and **Groq Cloud AI (Llama 3.3 70B Versatile)**, the bot processes natural language transaction descriptions and receipt/transaction screenshots to extract financial metadata, categorize expenses, and generate summary insights.

---

## 🏛️ System Architecture & Workflow

```text
  +-------------------------------------------------------------------------+
  |                        TELEGRAM USER INTERFACE                          |
  |  - User sends text ("Spent $45 on groceries") or receipt screenshot       |
  |  - Bot Username: @SpendSnap_kushagra_bot                                |
  +-------------------------------------------------------------------------+
                                       |
                                       | Telegram Bot API (python-telegram-bot)
                                       v
  +-------------------------------------------------------------------------+
  |                     TELEGRAM BOT ENGINE (bot/my_bot.py)                 |
  |  - Command Handlers (/start, /summary)                                  |
  |  - Message Handlers (filters.TEXT | filters.PHOTO)                      |
  |  - Formats incoming text into HumanMessage                              |
  +-------------------------------------------------------------------------+
                                       |
                                       | Invokes StateGraph Workflow
                                       v
  +-------------------------------------------------------------------------+
  |                 LANGGRAPH AI AGENT (backend/graph/workflow.py)           |
  |  - Compiled StateGraph Graph Execution (START -> welcome -> END)       |
  |  - State Schema: TypedDict graph_Schema with Annotated[List, add]       |
  |  - LLM Engine: Groq ChatGroq (model="llama-3.3-70b-versatile")           |
  +-------------------------------------------------------------------------+
                                       |
                                       | Formatted AI Response / Extraction
                                       v
  +-------------------------------------------------------------------------+
  |                    TELEGRAM RESPONSE & ACKNOWLEDGMENT                   |
  +-------------------------------------------------------------------------+
```

---

##  Core Features & Technical Highlights

### Agentic LangGraph StateGraph Workflow
* Built using **LangGraph** (`StateGraph`, `START`, `END`) to maintain stateful conversational execution streams.
* Uses **LangChain Core** (`HumanMessage`, `AIMessage`) and `TypedDict` schema annotation with list addition reducers.

### Groq Cloud Llama 3.3 70B LLM Integration
* Powered by `ChatGroq(model="llama-3.3-70b-versatile")` for high-throughput, low-latency financial entity extraction and reasoning.

### Telegram Bot Application (`python-telegram-bot`)
* Asynchronous event polling (`poll_interval=3`) supporting text and image attachments (`filters.TEXT | filters.PHOTO`).
* Slash commands:
  * `/start`: Welcomes user and displays usage instructions.
  * `/summary`: Trigger for expense aggregation and financial summary reports.

---

## Quick Start Guide

### Prerequisites
* **Python**: `3.10+`
* **Groq API Key**: Obtain from [Groq Cloud Console](https://console.groq.com/)
* **Telegram Bot Token**: Created via BotFather

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/Kusagra9308/SpendSnap.git
cd SpendSnap

# Create a virtual environment & activate it
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install python-telegram-bot langchain-groq langgraph langchain-core python-dotenv
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
TELEGRAM_BOT_TOKEN=8988159007:AAEDwRj9tnStkbEOvyf8MGZCPSnnFmp29yM
```

### 3. Run the Bot

```bash
python bot/my_bot.py
```
*Output:*
```text
Bot Starting ...
Polling Starting ...
```

---

## Project Structure

```text
SpendSnap/
├── backend/
│   └── graph/
│       └── workflow.py          # LangGraph StateGraph & Groq Llama 3.3 70B workflow
├── bot/
│   └── my_bot.py                # Telegram Bot handlers (/start, /summary, photo/text)
├── .gitlab-ci.yml               # CI/CD Pipeline configuration
└── README.md                    # Project documentation
```

---

## License

Distributed under the MIT License.
