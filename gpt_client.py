import openai
from config import OPENAI_API_KEY
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_user_input(user_message):
    prompt = f"""
    You are a helpful assistant that extracts key information from user messages for a food recommendation system.
    Extract the following information from the user's message if available:
    - Ingredients
    - Preferences
    - Location

    Provide the extracted information in JSON format with keys 'ingredients', 'preferences', and 'location'.

    User message: "{user_message}"
    """

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': prompt}]
    )

    return response['choices'][0]['message']['content'].strip()

def get_meal_options(ingredients, preferences, location, num_options):
    prompt = f"""
    You are a culinary expert providing meal suggestions.

    Based on the following inputs, suggest {num_options} meal options:

    Ingredients: {ingredients}
    Preferences: {preferences}
    Location: {location}

    Provide the suggestions in a numbered list with brief descriptions.

    Example:
    1. Chicken Stir Fry - A quick meal with chicken and vegetables.
    2. ...

    Begin:
    """

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': prompt}]
    )

    return response['choices'][0]['message']['content'].strip()

def get_recipe(meal_name):
    prompt = f"""
    You are a chef assistant.

    Provide a detailed recipe for "{meal_name}".

    Include ingredients and step-by-step instructions.

    Begin:
    """

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': prompt}]
    )

    return response['choices'][0]['message']['content'].strip()
