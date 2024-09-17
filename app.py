from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from config import BOT_PREFIX, NUM_OPTIONS
from conversation_manager import ConversationManager
from gpt_client import parse_user_input, get_meal_options, get_recipe

app = Flask(__name__)
conversation_manager = ConversationManager()

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender_id = request.values.get('From', '')
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg.lower().startswith(BOT_PREFIX):
        user_message = incoming_msg[len(BOT_PREFIX):].strip()

        if user_message.lower() in ['help', 'info']:
            help_message = ("🍽️ *Food Bot Help*\n"
                            "To get meal suggestions, simply type your message starting with /food followed by your preferences.\n"
                            "Example:\n"
                            "/food I have chicken and rice, and I want something spicy.\n"
                            "After receiving options, reply with the number or name of the meal to get the recipe.")
            msg.body(help_message)
            return str(resp)

        # Parse user input using GPT
        parsed_input = parse_user_input(user_message)

        # Handle JSON parsing
        try:
            import json
            parsed_data = json.loads(parsed_input)
            ingredients = parsed_data.get('ingredients', '')
            preferences = parsed_data.get('preferences', '')
            location = parsed_data.get('location', '')
        except json.JSONDecodeError:
            msg.body("Sorry, I couldn't understand your message. Please try again or type '/food help' for assistance.")
            return str(resp)

        # Get meal options
        options_text = get_meal_options(ingredients, preferences, location, NUM_OPTIONS)
        options_list = options_text.strip().split('\n')

        # Store options in conversation manager
        conversation_manager.update_user_options(sender_id, options_list)

        # Send options to user
        response_message = "Here are some meal options for you:\n\n" + options_text + "\n\nPlease reply with the number or name of the meal you'd like the recipe for."
        msg.body(response_message)
    else:
        # Check if the user is selecting an option
        user_options = conversation_manager.get_user_options(sender_id)
        if user_options:
            selected_option = incoming_msg.strip()
            # Match the user's selection
            selected_recipe = None
            for option in user_options:
                if option.startswith(selected_option + '.') or option.lower().find(selected_option.lower()) != -1:
                    selected_recipe = option.partition('. ')[2]  # Extract the meal name
                    break

            if selected_recipe:
                # Get recipe for the selected meal
                recipe = get_recipe(selected_recipe)
                msg.body(recipe)
                conversation_manager.clear_user_state(sender_id)
            else:
                msg.body("Sorry, I couldn't find that option. Please reply with the number or name of one of the meal options provided.")
        else:
            msg.body("Please start your message with '/food' to get meal suggestions. Type '/food help' for more information.")

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
