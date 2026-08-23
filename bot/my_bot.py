import os
import sys

# Add project root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tempfile
from typing import Final

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from backend.graph.workflow import first_graph

TOKEN: Final = "8988159007:AAEDwRj9tnStkbEOvyf8MGZCPSnnFmp29yM"
BOT_USERNAME: Final = "@SpendSnap_kushagra_bot"

# commands


# Start reply of telegram bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """👋 Welcome to SpendSnap!

I'm your AI-powered expense tracking assistant. Simply send a transaction screenshot, receipt image, or transaction details in text form.

For the best results, include a short caption describing the transaction. I'll automatically extract the relevant information, categorize the expense, and help you keep track of your spending.

Get started by sending your first transaction! 🚀"""
    )


# Summary reply of telegram bot
async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Fetching your expense summary. Please wait a moment..."
    )


# What to reply when message send
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Check  waiting for the user for category
    if "pending_amount" in context.user_data:
        amount = context.user_data.pop("pending_amount")
        category = update.message.text.strip()

        await update.message.reply_text(
            f"✅ Logged ₹{amount:.2f} under *{category}*!",
            parse_mode="Markdown"
        )
        return

    response = ""

    # if photo send
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        with tempfile.NamedTemporaryFile(
            suffix=".jpg", delete=False
        ) as temp_file:
            temp_path = temp_file.name

        try:
            await file.download_to_drive(temp_path)
            response = await handle_screenshot(temp_path)
        finally:
            try:
                os.remove(temp_path)
            except OSError:
                pass

    # if text send
    elif update.message.text:
        print("Sending llm request ...")
        timestamp = update.message.date.strftime("%Y-%m-%d %H:%M:%S %Z")
        response = handle_response(
            f"Message: {update.message.text} (Received at: {timestamp})"
        )
    else:
        print("SENDING REPLY")
        await update.message.reply_text("Unsupported message type.")
        return

    #Save pending_amount if category was missing and bot asked for clarification
    if response and "I recorded an expense of ₹" in response:
        import re
        match = re.search(r"₹([\d\.]+)", response)
        if match:
            context.user_data["pending_amount"] = float(match.group(1))

    if response:
        print("Sending reply ...")
        await update.message.reply_text(response)

# sending request to graph for text
def handle_response(text: str) -> str:

    print("Sending request to graph with image")

    reply = first_graph.invoke(
        {
            "input_type": "text",
            "text": text,
            "image_path": None,
        }
    )

    return reply["reply"][-1].content

# sending request to graph for image
async def handle_screenshot(image_path: str) -> str:

    print("Sending request to graph with image")

    reply = first_graph.invoke(
        {
            "input_type": "image",
            "text": None,
            "image_path": image_path,
        }
    )

    return reply["reply"][-1].content


# bot starting
if __name__ == "__main__":
    print("Bot Starting ...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("summary", summary))

    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))

    print("Polling Starting ...")
    app.run_polling(poll_interval=3)
