import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from typing import Dict, List
from datetime import datetime

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configure Google Gemini API
genai.configure(api_key='AIzaSyDC0qEt-RmlXLSCRxOVjw97CYKKtp6fif8')

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

# Store conversations: user_id -> list of (timestamp, role, content)
conversations: Dict[int, List[dict]] = {}

def store_message(user_id: int, role: str, content: str):
    """Store a message in the conversation history."""
    if user_id not in conversations:
        conversations[user_id] = []
    
    conversations[user_id].append({
        'timestamp': datetime.now().isoformat(),
        'role': role,
        'content': content
    })

def get_conversation_history(user_id: int, max_messages: int = 10) -> str:
    if user_id not in conversations:
        return ""
    
    recent_messages = conversations[user_id][-max_messages:]
    history = []
    for msg in recent_messages:
        role_prefix = "User: " if msg['role'] == 'user' else "Assistant: "
        history.append(f"{role_prefix}{msg['content']}")
    
    return "\n".join(history)

async def generate_response(user_id: int, prompt: str) -> str:
    try:
        history = get_conversation_history(user_id)

        full_prompt = (
            f"Previous conversation:\n{history}\n\n"
            f"Current user message: {prompt}\n\n"
            "Please provide a response that takes into account the conversation history if relevant."
        )
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "I'm sorry, I encountered an error while processing your request."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    welcome_message = 'Hello! I am your AI assistant. I can remember our conversation and use it for context in future responses. How can I help you today?'
    store_message(user_id, 'assistant', welcome_message)
    await update.message.reply_text(welcome_message)

async def alive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Yah! I am here only.. I can''t die that easily!😉')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_message = update.message.text
    logger.info(f"Received message from user {user_id}: {user_message}")

    store_message(user_id, 'user', user_message)

    ai_response = await generate_response(user_id, user_message)
    store_message(user_id, 'assistant', ai_response)
    
    logger.info(f"AI response to user {user_id}: {ai_response}")
    await update.message.reply_text(ai_response)

async def show_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    history = get_conversation_history(user_id)
    if history:
        await update.message.reply_text(f"Here's our recent conversation:\n\n{history}")
    else:
        await update.message.reply_text("We haven't had any conversation yet!")

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id in conversations:
        conversations[user_id].clear()
        await update.message.reply_text("Conversation history has been cleared!")
    else:
        await update.message.reply_text("No conversation history to clear!")

def main() -> None:
    # Initialize application
    application = Application.builder().token('7688969617:AAHMogPaXG_9P-g-Gn7POhXrFMEoX1cmYZc').build()

    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('alive', alive))
    application.add_handler(CommandHandler('history', show_history))
    application.add_handler(CommandHandler('clear', clear_history))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    logger.info("Chatbot Starting polling...")
    application.run_polling()

if __name__ == '__main__':
    print('Chatbot Starting...')
    try:
        main()
    except Exception as e:
        logger.error(f"An error occurred: {e}")