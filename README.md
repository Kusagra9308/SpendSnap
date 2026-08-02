# SpendSnap

## An AI-powered Telegram bot that automatically extracts, categorizes, and tracks your personal expenses from text messages and receipt screenshots.

---

## Project Description

Managing personal finances and manually logging daily transactions is tedious, error-prone, and often neglected. **SpendSnap** solves this problem by providing an intelligent, frictionless expense tracking assistant right inside Telegram. Built with an agentic **LangGraph** workflow, **LangChain**, and **Groq Cloud AI (Llama 3.3 70B Versatile)**, SpendSnap allows users to send simple natural language text (e.g., *"Spent $45 on groceries today"*) or upload receipt/transaction screenshots. The bot automatically extracts transaction amounts, categorizes spending (e.g., Food, Travel, Utilities), and formats the financial metadata for effortless expense tracking.

---

## Visual Aid / Demo

```text
  +-------------------------------------------------------------------------+
  |                        TELEGRAM USER INTERFACE                          |
  |  - User sends text ("Spent $45 on groceries") or receipt screenshot       |
  |  - Telegram Bot Handle: @SpendSnap_kushagra_bot                         |
  +-------------------------------------------------------------------------+
                                       |
                                       | Telegram Bot API (python-telegram-bot)
                                       v
  +-------------------------------------------------------------------------+
  |                     TELEGRAM BOT ENGINE (bot/my_bot.py)                 |
  |  - Command Handlers (/start, /summary)                                  |
  |  - Message & Photo Handlers (filters.TEXT | filters.PHOTO)              |
  |  - Formats incoming inputs for LangGraph state machine                  |
  +-------------------------------------------------------------------------+
                                       |
                                       | Invokes StateGraph Workflow
                                       v
  +-------------------------------------------------------------------------+
  |                 LANGGRAPH AI AGENT (backend/graph/workflow.py)           |
  |  - State Graph Execution (START -> choose -> welcome / welcome1 -> END) |
  |  - Structured Output Parsing via Pydantic ExpenseSchema                 |
  |  - LLM Engine: Groq ChatGroq (Llama 3.3 70B Versatile)                  |
  |  - OCR Engine: Tesseract OCR (Pillow / pytesseract)                     |
  +-------------------------------------------------------------------------+
```

<!-- DEMO PLACEHOLDER: Add your animated GIF or video walkthrough below -->
> 🎬 **Demo Video / Animated GIF Placeholder**
> 
> *(Insert your demo GIF or video link here: `![SpendSnap Demo](assets/spendsnap-demo.gif)`)*

---

## Prerequisites & Requirements

Before running SpendSnap, ensure your system meets the following requirements:

* **Python Version:** Python `3.10` or higher
* **Tesseract OCR Engine:** Required for image receipt parsing
  * **Windows:** Download and install Tesseract OCR (e.g., to `C:\Program Files\Tesseract-OCR\tesseract.exe`)
  * **Linux (Ubuntu/Debian):** `sudo apt-get install tesseract-ocr libtesseract-dev`
  * **macOS:** `brew install tesseract`
* **API Credentials:**
  * **Groq Cloud API Key:** Obtain from [Groq Console](https://console.groq.com/)
  * **Telegram Bot Token:** Generated via Telegram [@BotFather](https://t.me/botfather)

---

## Installation

Follow these sequential, copy-paste-ready commands to clone the repository and set up the project environment:

```bash
# 1. Clone the repository
git clone https://github.com/Kusagra9308/SpendSnap.git
cd SpendSnap

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install python-telegram-bot langchain-groq langgraph langchain-core pydantic Pillow pytesseract python-dotenv
```

### Configuration

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

## Usage Instructions

### 1. Launching the Telegram Bot

Execute the bot entry point from the project root directory:

```bash
python bot/my_bot.py
```

*Expected Terminal Output:*
```text
Bot Starting ...
Polling Starting ...
```

### 2. Interacting with the Bot in Telegram

Search for `@SpendSnap_kushagra_bot` in Telegram and interact using the following commands:

* **`/start`** — Displays the welcome message and instructions.
* **`/summary`** — Triggers the expense summary report.
* **Text Transaction Entry:** Send a message like `"Bought wireless headphones for $80"`.
* **Receipt Screenshot Entry:** Send a photo of a transaction receipt with an optional caption.

### Sample Code Block (LangGraph Agent Invocation)

```python
from backend.graph.workflow import first_graph

# Example: Invoking the agent with text input
response = first_graph.invoke({
    "input_type": "text",
    "text": "Paid $25 for Uber ride to airport",
    "image_path": None
})

# Returns structured Pydantic JSON output:
# {"amount": 25.0, "category": "Transportation", "transaction_date": null}
print(response["reply"][-1].content)
```

---

## Contributing Guidelines

Contributions are welcome! If you would like to contribute to SpendSnap:

1. **Fork the Repository:** Create your own feature branch (`git checkout -b feature/AmazingFeature`).
2. **Commit Your Changes:** Write clear, descriptive commit messages (`git commit -m 'Add AmazingFeature'`).
3. **Push to Branch:** Push your branch (`git push origin feature/AmazingFeature`).
4. **Open a Pull Request:** Describe your changes and reference any related issues.

For bug reports or feature requests, please open an issue on the [GitHub Issues](https://github.com/Kusagra9308/SpendSnap/issues) tab.

---

## License

Distributed under the **MIT License**. See `LICENSE` for details.
