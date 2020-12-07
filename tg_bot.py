import os
import logging
from detect_intent_texts import detect_intent_texts
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def reply_from_dialogflow(update: Update, context: CallbackContext) -> None:
    project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
    language_code = os.getenv("LANGUAGE_CODE")
    session_id = f'tg-{update.effective_user.id}'
    texts = update.message.text
    response = detect_intent_texts(
        project_id, session_id, texts, language_code)
    update.message.reply_text(response.query_result.fulfillment_text)


def main():
    """Start the bot."""
    load_dotenv()
    updater = Updater(token=os.getenv("TG_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, reply_from_dialogflow))
    updater.start_polling()


if __name__ == '__main__':
    main()
