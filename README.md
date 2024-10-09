
# Food Recommendation Bot

`what_to_eat` is a Telegram bot that provides personalized meal suggestions and recipes based on user inputs. Users can interact with the bot to get meal options, select recipes, and receive customized recommendations.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Bot](#running-the-bot)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **Personalized Meal Suggestions**: Get meal options based on ingredients, preferences, and location.
- **Detailed Recipes**: Receive recipes with ingredients and step-by-step instructions.
- **Group Chat Support**: Add the bot to Telegram groups for collaborative meal planning.
- **Conversation State Management**: The bot maintains conversation context for seamless interactions.

## Getting Started

### Prerequisites

- **Python 3.7+**
- **Telegram Account**
- **OpenAI API Key**: Sign up at [OpenAI](https://beta.openai.com/signup/) to obtain an API key.
- **Telegram Bot Token**: Create a bot using [@BotFather](https://telegram.me/BotFather) and obtain the API token.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/amritrajpaul/what_to_eat.git
   cd what_to_eat
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file or set environment variables in your system:

   ```bash
   OPENAI_API_KEY='your_openai_api_key'
   TELEGRAM_BOT_TOKEN='your_telegram_bot_token'
   ```

### Running the Bot

```bash
python bot.py
```

## Usage

### Start a Conversation with the Bot

Find your bot on Telegram using its username (e.g., @DishDeciderBot) and start a chat.

### Get Meal Suggestions

Send `/start` to initiate the conversation.

Type `/yumyoda` followed by your preferences.

**Example:**

```css
/food I have chicken and rice, and I want something spicy.
```

### Select a Meal Option

The bot will provide a list of meal options. Reply with the number or name of the meal to get the recipe.

### Receive the Recipe

The bot will send a detailed recipe, including ingredients and instructions.


## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the Repository**

   Click on the 'Fork' button at the top right corner of the repository page.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/amritrajpaul/what_to_eat.git
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**

   Implement your feature or bug fix.

5. **Commit and Push**

   ```bash
   git add .
   git commit -m "Description of your changes"
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**

   Go to the original repository on GitHub. Click on 'Pull Requests' and create a new pull request.

## Future Enhancements

We have exciting plans to enhance the bot's functionality. Contributions towards these features are highly appreciated!

1. **Shopping List Generation**
   - **Description**: Allow users to generate shopping lists based on selected recipes or meal plans.
   - **Implementation Ideas**:
     - Store selected recipes and ingredients.
     - Provide a command to output a consolidated shopping list.

2. **Scheduled Food Recommendations**
   - **Description**: Enable users to receive food recommendations or meal plans based on selected dates.
   - **Implementation Ideas**:
     - Implement a scheduling system to send recommendations at specified times.
     - Use Telegram's notification features or integrate with calendar services.

3. **Personalized Default Preferences**
   - **Description**: The bot learns from previous interactions to set default preferences for users.
   - **Implementation Ideas**:
     - Store user preferences and selected recipes.
     - Use machine learning to identify patterns and suggest personalized options.

4. **Multi-Language Support**
   - **Description**: Extend the bot's capabilities to support multiple languages.
   - **Implementation Ideas**:
     - Integrate language detection and translation services.
     - Localize meal suggestions and recipes.

5. **Dietary Restrictions and Allergens**
   - **Description**: Allow users to specify dietary restrictions or allergens to receive suitable recommendations.
   - **Implementation Ideas**:
     - Add options to set dietary preferences (e.g., vegetarian, gluten-free).
     - Filter recipes based on user-specified restrictions.

## License

This project is licensed under the MIT License.

## Acknowledgments

- **OpenAI**: For providing the GPT models used in the bot.
- **Telegram**: For offering the Bot API.
- **Contributors**: Thanks to everyone who has contributed to this project!
