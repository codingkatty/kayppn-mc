from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
import os
import requests

updater = Updater(os.environ["BOT_TOKEN"], use_context=True)

def help(update: Update, context: CallbackContext): 
    update.message.reply_text(
        "Available Commands:\n"
        "/mcstatus - Get server status\n"
    )

def mcstatus(update: Update, context: CallbackContext):
    try:
        response = requests.get('https://api.mcstatus.io/v2/status/java/kayppn.aternos.me:43010')
        data = response.json()
        version_name = data['version']['name_clean']
        if version_name == "● Offline":
            update.message.reply_text("Server Offline 🥲")
        else:
            update.message.reply_text("CHAT ITS ONLINE GOGOGO!!")
    except Exception as e:
        update.message.reply_text(f"Error getting server status: {str(e)}")

updater.dispatcher.add_handler(CommandHandler('mcstatus', mcstatus))
updater.start_polling()