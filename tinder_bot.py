import json
import logging

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, User
from telegram import InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

with open("config.json", "r") as f:
    conf = json.load(f)["tinder_bot"]
    TOKEN = conf["token"]
    BOT_NAME = conf["bot_name"]
    USERNAME = conf["username"]


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

keyboard = [
    [
        InlineKeyboardButton("Dislike", callback_data="dislike"),
        InlineKeyboardButton("Like", callback_data="like"),
    ]
]

reply_markup = InlineKeyboardMarkup(keyboard)


def start(bot, update: Update):

    user: User = update.effective_user

    if user.username == USERNAME:
        update.message.reply_media_group([InputMediaPhoto("")])
        update.message.reply_text("Please choose:", reply_markup=reply_markup)
    else:
        update.message.reply_text(f"You should not be here, {user.username}")


def button(bot, update):
    query = update.callback_query
    # query.data

    bot.send_media_group(media=[InputMediaPhoto()], chat_id=query.message.chat_id)
    bot.send_message(
        text="Please choose:", reply_markup=reply_markup, chat_id=query.message.chat_id
    )


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    bot = telegram.Bot(TOKEN)
    updater = Updater(bot=bot)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(pattern="like", callback=button))
    updater.dispatcher.add_handler(CallbackQueryHandler(pattern="dislike", callback=button))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == "__main__":
    main()
