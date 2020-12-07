import os
import logging
import traceback
import html
import json
from detect_intent_texts import detect_intent_texts
from dotenv import load_dotenv
from telegram import Update, ParseMode
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext)


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


def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(
        msg="Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    context.bot.send_message(chat_id=os.getenv("DEVELOPER_CHAT_ID"), text=message, parse_mode=ParseMode.HTML)


def main():
    """Start the bot."""
    load_dotenv()
    updater = Updater(token=os.getenv("TG_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_error_handler(error_handler)

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, reply_from_dialogflow))
    updater.start_polling()


if __name__ == '__main__':
    main()
