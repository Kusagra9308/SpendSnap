import sys
import os

# Add project root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Final
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from backend.graph.workflow import first_graph
from langchain_core.messages import AIMessage, HumanMessage

TOKEN: Final = "8988159007:AAEDwRj9tnStkbEOvyf8MGZCPSnnFmp29yM"
BOT_USERNAME: Final = "@SpendSnap_kushagra_bot"

# commands


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """👋 Welcome to SpendSnap!

I'm your AI-powered expense tracking assistant. Simply send a transaction screenshot, receipt image, or transaction details in text form.

For the best results, include a short caption describing the transaction. I'll automatically extract the relevant information, categorize the expense, and help you keep track of your spending.

Get started by sending your first transaction! 🚀"""
    )


async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Fetching your expense summary. Please wait a moment..."
    )


# response


def handle_response(text: str) -> str:

    processed : HumanMessage =  HumanMessage(content=text)

    print("Getting response from llm ...")

    reply = first_graph.invoke({"message": [processed]})
    
    message_list = reply["message"]

    final_message = message_list[-1]
    
    if hasattr(final_message, "content"):
        return final_message.content
    else:
        return str(final_message)


async def handle_screenshot():
    return "✅ Saved"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        response = await handle_screenshot()
        await update.message.reply_text(response)
    elif update.message.text:
        print("Send llm request ...")
        response: str = handle_response(update.message.text)
        if response:
            print("Sending reply ...")
            await update.message.reply_text(response)
    else:
        await update.message.reply_text("Unsupported message type.")


if __name__ == "__main__":
    print("Bot Starting ...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("summary", summary))

    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
    
    print("Polling Starting ...")
    app.run_polling(poll_interval=3)
