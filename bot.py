import logging
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
from config import TELEGRAM_BOT_TOKEN, BOT_PREFIX, NUM_OPTIONS
from conversation_manager import ConversationManager
from gpt_client import parse_user_input, get_meal_options, get_recipe
import json
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Conversation Manager
conversation_manager = ConversationManager()

# Define conversation states
CHOOSING, TYPING_REPLY = range(2)

async def start(update: Update, context: CallbackContext) -> int:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm your Food Recommendation Bot.\n"
        f"Type '{BOT_PREFIX}' followed by your preferences to get meal suggestions.\n"
        f"Example:\n{BOT_PREFIX} I have chicken and rice, and I want something spicy."
    )
    return CHOOSING

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a help message when the command /help is issued."""
    help_message = (
        "🍽️ *Food Recommendation Bot Help* 🍽️\n\n"
        "You can use this bot to get personalized meal suggestions based on ingredients you have, your preferences, and other information. Here's how you can use the bot:\n\n"
        "1️⃣ *Get Meal Suggestions*\n"
        f"Simply start your message with `{BOT_PREFIX}` followed by a description of what you have or what you're craving.\n"
        "_Examples:_\n"
        f"`{BOT_PREFIX} I have chicken and potatoes, suggest something spicy.`\n"
        f"`{BOT_PREFIX} I want a quick and healthy dinner.`\n\n"
        
        "2️⃣ *Provide Ingredients in Your Fridge*\n"
        "Tell me what ingredients you have in your fridge, and I will suggest meals using those ingredients.\n"
        "_Example:_\n"
        f"`{BOT_PREFIX} I have eggs, tomatoes, and cheese. What can I make?`\n\n"

        "3️⃣ *Meal Type and Cuisine*\n"
        "You can specify the type of meal you're looking for (e.g., breakfast, lunch, dinner) and the cuisine you prefer (e.g., Indian, Bengali, Chinese).\n"
        "_Examples:_\n"
        f"`{BOT_PREFIX} Suggest a Bengali dinner option.`\n"
        f"`{BOT_PREFIX} I want an Indian breakfast using potatoes.`\n\n"

        "4️⃣ *Get a Recipe*\n"
        "After receiving meal suggestions, reply with the number or name of the meal to get a detailed recipe.\n"
        "_Example:_\n"
        "`2` or `Chicken Stir Fry`\n\n"
        
        "💡 *Tip:* You can keep your instructions simple or provide more details to get more accurate suggestions.\n\n"
        "Feel free to ask for help anytime by typing `/help`!"
    )
    await update.message.reply_text(help_message, parse_mode='Markdown')

async def handle_message(update: Update, context: CallbackContext) -> int:
    """Handle user messages."""
    user_message = update.message.text.strip()
    user_id = update.effective_user.id
    print(f"Received message: {user_message}")

    # Check if the message starts with the bot prefix
    if user_message.lower().startswith(BOT_PREFIX):
        user_query = user_message[len(BOT_PREFIX):].strip()
        print(f"Received {BOT_PREFIX} command with message: {user_message}")  # Log message received
        # Parse user input using GPT
        parsed_input = parse_user_input(user_query)

        if parsed_input is None:
            print("Failed to get a valid response from GPT")
            await update.message.reply_text("Sorry, I couldn't process your request at the moment. Please try again later.")
            return CHOOSING
        
        # Handle JSON parsing
        try:
            parsed_data = json.loads(parsed_input)
            print(f"Parsed Data: {parsed_data}")  # Log parsed data
            ingredients = parsed_data.get('ingredients', '')
            preferences = parsed_data.get('preferences', '')
            location = parsed_data.get('location', '')
            meal_type = parsed_data.get('meal_type', '')  
            cuisine_type = parsed_data.get('cuisine_type', '')
        except json.JSONDecodeError as e:
            print(f"JSON Parsing Error: {e}")  # Log any JSON parsing issues    
            await update.message.reply_text(
                "Sorry, I couldn't understand your message. Please try again or type '/help' for assistance."
            )
            return CHOOSING
         # Log what values are being sent to get_meal_options
        print(f"Getting meal options with: ingredients={ingredients}, preferences={preferences}, location={location}, meal_type={meal_type}, cuisine_type={cuisine_type}")

        # Get meal options
        options_text = get_meal_options(ingredients, preferences, location, meal_type, cuisine_type, NUM_OPTIONS)
        options_list = options_text.strip().split('\n')

        # Store options in conversation manager
        conversation_manager.update_user_options(user_id, options_list)

        # Send options to user
        response_message = "Here are some meal options for you:\n\n" + options_text + "\n\nPlease reply with the number or name of the meal you'd like the recipe for."
        await update.message.reply_text(response_message)
        return TYPING_REPLY
    else:
        # Check if the user is selecting an option
        user_options = conversation_manager.get_user_options(user_id)
        if user_options:
            selected_option = user_message.strip()
            # Match the user's selection
            selected_recipe = None
            for option in user_options:
                if option.startswith(selected_option + '.') or selected_option.lower() in option.lower():
                    selected_recipe = option.partition('. ')[2]  # Extract the meal name
                    break

            if selected_recipe:
                # Get recipe for the selected meal
                recipe = get_recipe(selected_recipe)
                await update.message.reply_text(recipe)
                conversation_manager.clear_user_state(user_id)
                return ConversationHandler.END
            else:
                await update.message.reply_text(
                    "Sorry, I couldn't find that option. Please reply with the number or name of one of the meal options provided."
                )
                return TYPING_REPLY
        else:
            await update.message.reply_text(
                f"Please start your message with '{BOT_PREFIX}' to get meal suggestions. Type '/help' for more information."
            )
            return CHOOSING

async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text('Goodbye!')
    return ConversationHandler.END

def main() -> None:
    """Start the bot."""
    # Use ApplicationBuilder to create the bot application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Define conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
            TYPING_REPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('help', help_command)],
    )

    # Add conversation handler to the application
    application.add_handler(conv_handler)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    print('start')
    main()
