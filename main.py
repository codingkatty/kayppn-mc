from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
import os
import requests
import random
from supabase import create_client, Client

# Initialise Supabase
supabase_url = "https://msfutgjgflgkckxreksp.supabase.co"
supabase_key = os.environ["SUPABASE_KEY"]
supabase: Client = create_client(supabase_url, supabase_key)

updater = Updater(os.environ["BOT_TOKEN"], use_context=True)

def help(update: Update, context: CallbackContext): 
    update.message.reply_text(
        "Available Commands:\n"
        "/setserver - Configure server address\n"
        "/mcstatus - Get server status\n"
        "/setcoords <x> <z> <remark> - Note coordinates\n"
        "/getcoords - Get noted coordinates\n"
    )

def setserver(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)

    if not context.args:
        update.message.reply_text("Usage: /setserver <address>")
        return

    server_address = context.args[0]
    data = {"chat_id": chat_id, "server_address": server_address}
    
    try:
        response = supabase.from_("servers").upsert(data, on_conflict=["chat_id"]).execute()
        if response.status == 200:
            update.message.reply_text(f"Server address set to {server_address} for this chat.")
        else:
            update.message.reply_text("Failed to set server address. Please try again.")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def mcstatus(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)
    try:
        response = supabase.from_("servers").select("server_address").eq("chat_id", chat_id).execute()
        if not response.data:
            update.message.reply_text("Server address not configured. Use /setserver <address> to set it.")
            return

        server_address = response.data[0]["server_address"]
        
        api_response = requests.get(f'https://api.mcstatus.io/v2/status/java/{server_address}')
        data = api_response.json()
        version_name = data.get('version', {}).get('name_clean', 'Unknown')
        
        if version_name == "● Offline":
            responses = [
                "Server Offline 🥲",
                "Server is ded.",
                "Nope not the time yet."
            ]
            update.message.reply_text(random.choice(responses))
        else:
            responses = [
                "CHAT ITS ONLINE GOGOGO!!",
                "Your life is on the line.",
                "Line up in queue."
            ]
            update.message.reply_text(random.choice(responses))
    except Exception as e:
        update.message.reply_text(f"Error getting server status: {str(e)}")

def setcoords(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)

    if len(context.args) < 3:
        update.message.reply_text("Usage: /setcoords <x> <z> <remark>")
        return

    try:
        x = float(context.args[0])
        z = float(context.args[1])
        remark = " ".join(context.args[2:])
        data = {"chat_id": chat_id, "x": x, "z": z, "remark": remark}
        
        response = supabase.from_("coordinates").insert(data).execute()
        
        if response.status == 201:
            update.message.reply_text(f"Coordinates set to (x: {x}, z: {z}) with remark: {remark}")
        else:
            update.message.reply_text("Failed to set coordinates. Please try again.")
    except ValueError:
        update.message.reply_text("Invalid coordinates. Please use numbers for x and z.")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def getcoords(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)
    try:
        response = supabase.from_("coordinates").select("*").eq("chat_id", chat_id).execute()
        
        if not response.data:
            update.message.reply_text("No coordinates found. Use /setcoords <x> <z> <remark> to add coordinates.")
            return

        coords_list = "\n".join([f"(x: {coord['x']}, z: {coord['z']}) - {coord['remark']}" for coord in response.data])
        update.message.reply_text(f"Stored Coordinates:\n{coords_list}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# Bind commands
updater.dispatcher.add_handler(CommandHandler('setserver', setserver))
updater.dispatcher.add_handler(CommandHandler('mcstatus', mcstatus))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('setcoords', setcoords))
updater.dispatcher.add_handler(CommandHandler('getcoords', getcoords))
updater.start_polling()
updater.idle()