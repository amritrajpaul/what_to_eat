from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from flask_session import Session
import re
import logging
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
app.config['SESSION_TYPE'] = 'filesystem'  # Using filesystem for simplicity
Session(app)

openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace with your OpenAI API key

logging.basicConfig(level=logging.INFO)

# Store user sessions
user_sessions = {}

@app.route('/', methods=['GET'])
def home():
    return 'The WhatsApp bot is running!', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')
    resp = MessagingResponse()
    msg = resp.message()

    # Logging incoming message
    logging.info(f"Received message from {sender}: {incoming_msg}")

    # Check if the user has an ongoing session
    if sender not in user_sessions:
        user_sessions[sender] = {'state': 'INITIAL', 'options': [], 'selected_option': None}

    user_session = user_sessions[sender]

    # State machine to handle conversation flow
    if user_session['state'] == 'INITIAL':
        # Start of conversation
        if incoming_msg.lower().startswith('/food'):
            user_message = incoming_msg[len('/food'):].strip()
            # Use GPT to parse the user's message
            ingredients, preferences, location = parse_user_input(user_message)
            # Generate meal options
            meal_options = generate_meal_options(ingredients, preferences, location)
            if meal_options:
                user_session['options'] = meal_options
                user_session['state'] = 'AWAITING_SELECTION'

                # Send meal options to the user
                options_message = "Here are some meal options based on your input:\n"
                for idx, option in enumerate(meal_options, 1):
                    options_message += f"{idx}. {option}\n"

                options_message += "\nPlease select an option by number or name."
                msg.body(options_message)
            else:
                msg.body("Sorry, I couldn't find any meal suggestions based on your input. Please try again with different ingredients or preferences.")
        else:
            # Provide usage instructions
            instructions = """
            🍽️ *Welcome to the Food Bot!* 🍽️

            To get meal suggestions, simply send a message starting with /food followed by your cravings or ingredients you have.

            *Examples:*
            - /food I'm in the mood for something spicy with chicken.
            - /food I have pasta and tomatoes. What can I make?
            - /food Suggest meals with rice and vegetables.

            I'll provide you with meal options, and you can select one to get the recipe!

            """
            msg.body(instructions)
    elif user_session['state'] == 'AWAITING_SELECTION':
        # User selects a meal option
        selected_recipe = match_user_selection(incoming_msg, user_session['options'])
        if selected_recipe:
            # Retrieve recipe details
            recipe_details = get_recipe_details(selected_recipe)
            msg.body(recipe_details)
            # Reset the user's session
            user_sessions[sender] = {'state': 'INITIAL', 'options': [], 'selected_option': None}
        else:
            msg.body("Sorry, I didn't understand your selection. Please choose an option by number or name from the list provided.")
    else:
        # Reset session in case of unexpected state
        user_sessions[sender] = {'state': 'INITIAL', 'options': [], 'selected_option': None}
        msg.body("Let's start over. Send '/food' followed by your preferences to get meal suggestions.")

    return str(resp)

def parse_user_input(user_message):
    # Use OpenAI GPT to extract ingredients, preferences, and location
    prompt = f"""
    Extract the ingredients, preferences, and location from the following message. If any of them are not mentioned, return them as empty.

    Message: "{user_message}"

    Format your response as JSON:
    {{
        "ingredients": "...",
        "preferences": "...",
        "location": "..."
    }}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts information from user messages."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0,
        )

        answer = response.choices[0].message['content'].strip()

        # Parse the JSON response
        data = json.loads(answer)
        ingredients = data.get('ingredients', '')
        preferences = data.get('preferences', '')
        location = data.get('location', '')

    except Exception as e:
        logging.error(f"Error parsing user input: {e}")
        # Default to empty values if parsing fails
        ingredients = ''
        preferences = ''
        location = ''

    return ingredients, preferences, location

def generate_meal_options(ingredients, preferences, location):
    # Use GPT to generate meal options
    prompt = f"""
    Based on the following inputs, suggest 5 meal options. List them in a numbered format.

    Ingredients: {ingredients}
    Preferences: {preferences}
    Location: {location}

    Only provide the names of the meals.

    Example:
    1. Spaghetti Bolognese
    2. Chicken Curry
    3. ...

    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a culinary expert providing meal suggestions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.7,
        )

        answer = response.choices[0].message['content'].strip()
        # Extract meal options from the answer
        meal_options = extract_meal_options(answer)
    except Exception as e:
        logging.error(f"Error generating meal options: {e}")
        meal_options = []

    return meal_options

def extract_meal_options(gpt_response):
    # Extract meal names from GPT response
    options = []
    lines = gpt_response.split('\n')
    for line in lines:
        match = re.match(r'\d+\.\s*(.*)', line)
        if match:
            option = match.group(1).strip()
            options.append(option)
        else:
            # Handle cases where numbering is not provided
            if line.strip():
                options.append(line.strip())
    return options

def match_user_selection(user_input, options):
    user_input = user_input.strip().lower()
    # Try to match by number
    if user_input.isdigit():
        index = int(user_input) - 1
        if 0 <= index < len(options):
            return options[index]
    # Try to match by name
    for option in options:
        if user_input in option.lower():
            return option
    return None

def get_recipe_details(recipe_name):
    # Use GPT to get recipe details
    prompt = f"""
    Provide a detailed recipe for "{recipe_name}". Include ingredients and step-by-step instructions.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a culinary expert providing detailed recipes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )

        recipe_details = response.choices[0].message['content'].strip()
    except Exception as e:
        logging.error(f"Error getting recipe details: {e}")
        recipe_details = "Sorry, I couldn't retrieve the recipe at this time."

    return recipe_details

if __name__ == '__main__':
    app.run(debug=True)
