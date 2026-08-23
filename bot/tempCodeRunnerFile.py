
BOT_USERNAME: Final = "@SpendSnap_kushagra_bot"

# commands


# Start reply of telegram bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """👋 Welcome to SpendSnap!
