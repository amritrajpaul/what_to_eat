import openai
from config import OPENAI_API_KEY
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

# print('apikeyyyyyyyyyyy',os.getenv("OPENAI_API_KEY"))
# response = openai.ChatCompletion.create(
#             model='gpt-3.5-turbo',
#             messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
#                     {'role': 'user', 'content': 'are you working and what is the meaning of life?'}]
#         )
# result = response['choices'][0]['message']['content'].strip()
# print(f"GPT Response: {result}")

def parse_user_input(user_message):
    # mock_response = json.dumps({
    #     "ingredients": "chicken",
    #     "preferences": "spicy",
    #     "location": "home",
    #     "meal_type": "dinner",
    #     "cuisine_type": "Indian"
    # })
    # print(f"Mocked Response: {mock_response}")
    # return mock_response
    prompt = f"""
    You are a helpful assistant that extracts key information from user messages for a food recommendation system.
    Extract the following information from the user's message if available:
    - Ingredients
    - Preferences
    - Location
    - Meal Type (e.g., breakfast, lunch, dinner)
    - Cuisine Type (e.g., Indian, Bengali)

    Provide the extracted information in JSON format with keys 'ingredients', 'preferences', 'location', 'meal_type', and 'cuisine_type'.

    User message: "{user_message}"
    """
    print(f"Generated Prompt: {prompt}")  # Log the prompt being sent
    print(f"Using OpenAI API Key: {OPENAI_API_KEY}")
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': prompt}]
        )

        result = response['choices'][0]['message']['content'].strip()
        print(f"GPT Response: {result}")  # Debugging log
        return result
    except Exception as e:
        print(f"Error with OpenAI API: {e}")  # Log any API errors
        return None

def get_meal_options(ingredients, preferences, location, meal_type, cuisine_type, num_options):
    prompt = f"""
    You are a culinary expert providing meal suggestions.

    Based on the following inputs, suggest {num_options} meal options:

    Ingredients: {ingredients}
    Preferences: {preferences}
    Location: {location}
    Meal Type: {meal_type}
    Cuisine Type: {cuisine_type}

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
