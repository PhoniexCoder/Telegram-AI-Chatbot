# Telegram-AI-Chatbot
This project is a Telegram chatbot powered by Google's Gemini API, designed to provide intelligent, context-aware responses in both group chats and private messages. The bot stores conversation history and leverages it to generate relevant, coherent replies based on previous interactions.
### Features:
- **AI-Powered Responses:** The bot uses Google Gemini API to generate natural, intelligent responses.
- **Conversation Memory:** The bot stores conversation history and uses it to provide context-aware responses.
- **Supports Group and Private Chats:** The bot works both in group chats (with customizable settings) and private messages.
- **Customizable Settings for Group Chats:** Admins can set behaviors such as always replying or limiting the number of recent messages used for context.
- **Error Handling and Logging:** The bot includes error management to ensure smooth operation, along with logging for debugging.

## How to Use

### Deploying the Bot
1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/telegram-ai-assistant.git
    cd telegram-ai-assistant
    ```

2. **Install Dependencies:**
    The project uses Python and requires the `python-telegram-bot` and `google-generativeai` libraries.
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Google Gemini API Key:**
    You’ll need to obtain an API key from Google Gemini. Set your API key in the script where it's referenced:
    ```python
    genai.configure(api_key='your-api-key-here')
    ```

4. **Create a Telegram Bot:**
    - Talk to [BotFather](https://core.telegram.org/bots#botfather) on Telegram to create a new bot.
    - Copy the generated API token.

5. **Set Up Telegram Token:**
    Set your bot's token in the code:
    ```python
    application = Application.builder().token('your-bot-token-here').build()
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

## License
