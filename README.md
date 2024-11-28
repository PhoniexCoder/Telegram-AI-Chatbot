# Telegram AI Chatbot

This repository contains a Telegram-based AI chatbot that leverages Google's Gemini API to engage users in conversations. The bot is available in two versions:

1. **Version 1** - DM Support Only
2. **Version 2** - Group and DM Support

The bot can be interacted with by users to get intelligent responses based on their messages.

You can interact with the bot by visiting [this link](https://t.me/convospark_bot).

## Features

### Version 1: DM Support Only
- **Start**: Initializes the conversation with a welcome message.
- **Alive**: Checks if the bot is online and responds.
- **History**: Displays the recent conversation history.
- **Clear**: Clears the conversation history.

This version supports only Direct Messages (DM) with the bot.

### Version 2: Group and DM Chat Support
- **Start**: Initializes the conversation with a welcome message.
- **Alive**: Checks if the bot is online and responds.
- **Settings**: Available for group chats. Allows admins to configure bot settings (e.g., always replying, max message history).
- **Forget**: Clears the conversation history (in both group and DM chats).

Version 2 supports both Group Chats and Direct Messages. It allows group admins to control bot behavior via settings.

## Bot Commands

### Version 1 (DM Only):
- `/start`: Start the conversation with the bot.
- `/alive`: Check if the bot is online and responding.
- `/history`: View the most recent conversations.
- `/clear`: Clear the conversation history.

### Version 2 (Group + DM Support):
- `/start`: Start the conversation with the bot.
- `/alive`: Check if the bot is online and responding.
- `/settings`: Used by group admins to set bot behavior (e.g., enabling/disabling replies in groups).
- `/forget`: Clears all the conversation history, both in group chats and DMs.

## How to Run

To run this bot on your own server:

1. Clone this repository to your local machine or server:
   ```bash
   git clone https://github.com/PhoniexCoder/Telegram-AI-Chatbot.git
    ```

2. **Install Dependencies:**
    The project uses Python and requires the `python-telegram-bot` and `google-generativeai` libraries.
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Google Gemini API Key:**
    You’ll need to obtain an API key from Google Gemini. Set your API key in the script where it's referenced:
    ```python
    genai.configure(api_key='YOUR_API_KEY')
    ```

4. **Create a Telegram Bot:**
    - Talk to [BotFather](https://core.telegram.org/bots#botfather) on Telegram to create a new bot.
    - Copy the generated API token.

5. **Set Up Telegram Token:**
    Set your bot's token in the code:
    ```python
    application = Application.builder().token('TELEGRAM_BOT_TOKEN').build()
    ```

6. **Run the Bot:**
    After setting up the dependencies and credentials, you can run the bot:
    ```bash
    python bot.py
    ```

### Available Commands
- `/start` – Initializes the bot and sends a welcome message.
- `/alive` – Checks if the bot is online.
- `/settings max_messages <number>` – Configures the number of past messages to consider for context.
- `/settings always_reply <true/false>` – Configures whether the bot should always reply in group chats.
- `/clear` – Clears the conversation history.

### Bot Behavior in Group Chats
- **Mentioning the Bot:** The bot will respond when mentioned in group chats. If the `always_reply` setting is enabled, the bot will reply to all messages.
- **Private Chats:** The bot will always respond in private messages.

## Example Conversation

1. User: "Hello, bot!"
2. Bot: "Hello! I am your AI assistant. How can I help you today?"

1. User: "What's the weather like today?"
2. Bot: "Sorry, I don't have access to weather data at the moment, but I can assist with other tasks."

## Contributions
Feel free to fork the project and contribute by submitting pull requests. For issues, please open an issue on the [GitHub Issues page](https://github.com/your-username/telegram-ai-assistant/issues).
