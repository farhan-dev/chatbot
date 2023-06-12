from fastapi import FastAPI
import telegram

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import random
import string

def generate_code():
    code_length = 6  # Length of the generated code
    characters = string.ascii_uppercase + string.digits  # Characters used for the code

    code = ''.join(random.choices(characters, k=code_length))
    return code

app = FastAPI()

# Initialize the Telegram bot
bot_token = "5820492527:AAGO7jcjZWADDKgPPPJB8FlWUXoGBqSF3Hc"
bot = telegram.Bot(token=bot_token)
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Register command handlers
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the registration bot! Please provide your name and email separated by a comma.")
dispatcher.add_handler(CommandHandler("start", start))


def register_user(name, email):
    # Perform user registration logic here
    # Replace with your own registration implementation
    return True  # Assuming registration is successful

def process_message(update, context):
    user_input = update.message.text
    print (user_input.split(',',1)),
    # Extract name and email from the user's input
    try:
        creds = list (map(str.strip, user_input.split(',',1)))
        print (creds)

        # Check if name and email are provided
        if not creds[0] or not creds[1]:
            raise ValueError("Name and email cannot be empty.")
        name=creds[0]
        email=creds[1]

        # Register the user on the server and generate a code
        registration_success = register_user(name, email)
        if registration_success:
            # Generate a code for the user
            code = generate_code()

            response = f"You have been registered! Your code is {code}."
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Registration failed. Please try again later.")
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred during registration. Please try again later.")
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_message))

# Start the Telegram bot
updater.start_polling()

@app.get("/")
def read_root():
    return {"Hello": "World"}



