from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
import os
import requests
import random
from supabase import create_client, Client

"""
 * Minecraft Telegram Bot by Candy
 *
 * This bot is made because I face many issues while playing on the server with my friends.
 * Main issue being not able to know if the server is online or offline, which sometime is just a waste of time to ask/check.
 * By adding this bot to our group, we get to instantly check our server status.
 *
 * Special thanks: Raff for suggesting the coord list idea <3
 * Hosted on Railway
"""

# Initialise Supabase
supabase_url = "https://msfutgjgflgkckxreksp.supabase.co"
supabase_key = os.environ["SUPABASE_KEY"]
supabase: Client = create_client(supabase_url, supabase_key)

updater = ApplicationBuilder(os.environ["BOT_TOKEN"], use_context=True)

# Onboarding message
def start(update: Update, context: CallbackContext): 
    update.message.reply_text("Hey there fellow Minecrafter! Use /help to see a list of available commands.")

# List of commands
def help(update: Update, context: CallbackContext): 
    update.message.reply_text(
        "Available Commands:\n"
        "/setserver <address> - Configure server address (Artenos only)\n"
        "/mcstatus - Get server status\n"
        "/setcoords <x> <z> <remark> [overworld/nether] - Note coordinates\n"
        "/getcoords - Get noted coordinates\n"
        "/convertcoords <x> <z> [overworld/nether] - Convert coords to the other dimension\n"
    )

# Configure server address (specific chat)
def setserver(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)

    if not context.args:
        update.message.reply_text("Usage: /setserver <address>")
        return

    server_address = context.args[0]
    data = {"chat_id": chat_id, "server_address": server_address}
    
    try:
        supabase.from_("servers").upsert(data, on_conflict=["chat_id"]).execute()
        update.message.reply_text(f"Server address set to {server_address} for this chat.")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# Gets the status of server (on/off)
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
        online_status = data.get('online')
        version_name = data.get('version', {}).get('name_clean', 'Unknown')
        
        if version_name == "● Offline" or not online_status:
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

# Add a coordinate
def setcoords(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)

    if len(context.args) < 3:
        update.message.reply_text("Usage: /setcoords <x> <z> <remark> [overworld/nether]")
        return

    try:
        x = float(context.args[0])
        z = float(context.args[1])
        if context.args[-1] == 'overworld' or context.args[-1] == 'nether':
            remark = " ".join(context.args[2:-1])
            dimension = context.args[-1]
        else:
            remark = " ".join(context.args[2:])
            dimension = 'overworld'
        
        data = {"chat_id": chat_id, "x": x, "z": z, "remark": remark,"dimension":dimension}
        
        supabase.from_("coordinates").insert(data).execute()
        update.message.reply_text(f"Coordinates set to (x: {x}, z: {z}) with remark: {remark}")
    except ValueError:
        update.message.reply_text("Invalid coordinates. Please use numbers for x and z.")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# Get a list of coordinates
def getcoords(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)
    try:
        response = supabase.from_("coordinates").select("*").eq("chat_id", chat_id).execute()
        
        if not response.data:
            update.message.reply_text("No coordinates found. Use /setcoords <x> <z> <remark> to add coordinates.")
            return

        coords_list = "\n".join([f"(x: {coord['x']}, z: {coord['z']}) - {coord['remark']} [{coord['dimension']}]" for coord in response.data])
        update.message.reply_text(f"Stored Coordinates:\n{coords_list}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")
        
def convertcoords(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)
    try:
        x = float(context.args[0])
        z = float(context.args[1])
        if context.args[-1] == 'overworld' or context.args[-1] == 'nether':
            remark = " ".join(context.args[2:-1])
            dimension = context.args[-1]
        else:
            remark = " ".join(context.args[2:])
            dimension = 'overworld'
        if (dimension == 'overworld'):
            update.message.reply_text(f"Coordinates equivalent in the nether is x: {x/8}, z: {z/8}")
        else:
            update.message.reply_text(f"Coordinates equivalent in the overworld is x: {x*8}, z: {z*8}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# Bind commands
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('setserver', setserver))
updater.dispatcher.add_handler(CommandHandler('mcstatus', mcstatus))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('setcoords', setcoords))
updater.dispatcher.add_handler(CommandHandler('getcoords', getcoords))
updater.dispatcher.add_handler(CommandHandler('convertcoords', convertcoords))
updater.start_polling()
updater.idle()
