import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from typing import Dict, List
from datetime import datetime

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configure Google Gemini API
genai.configure(api_key='AIzaSyDC0qEt-RmlXLSCRxOVjw97CYKKtp6fif8')
model = genai.GenerativeModel('gemini-pro')

# Store conversations and group settings
conversations: Dict[int, List[dict]] = {}
group_settings: Dict[int, dict] = {}

def store_message(chat_id: int, user_id: int, role: str, content: str):

    if chat_id not in conversations:
        conversations[chat_id] = []
    
    conversations[chat_id].append({
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'role': role,
        'content': content
    })
    
    # Trim conversation history
    conversations[chat_id] = conversations[chat_id][-50:]

def get_conversation_history(chat_id: int, max_messages: int = 10) -> str:

    if chat_id not in conversations:
        return ""
    
    recent_messages = conversations[chat_id][-max_messages:]
    history = []
    for msg in recent_messages:
        role_prefix = f"User {msg['user_id']}: " if msg['role'] == 'user' else "Bot: "
        history.append(f"{role_prefix}{msg['content']}")
    
    return "\n".join(history)

async def generate_response(chat_id: int, user_id: int, prompt: str) -> str:
    try:
        history = get_conversation_history(chat_id)
        
        # Create a prompt that includes conversation history
        full_prompt = (
            f"Previous conversation:\n{history}\n\n"
            f"Current user message: {prompt}\n\n"
            "Please provide a concise, relevant response."
        )
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "I'm sorry, I encountered an error while processing your request."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    welcome_message = 'Hello! I am your AI assistant. How can I help you today?'
    store_message(chat_id, user_id, 'assistant', welcome_message)
    await update.message.reply_text(welcome_message)

async def alive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Yah! I am here only.. I can''t die that easily!😉')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_message = update.message.text
    is_group = update.message.chat.type in ['group', 'supergroup']
    
    # Check group-specific settings
    bot_username = context.bot.username
    is_mentioned = is_group and f'@{bot_username}' in user_message
    always_reply = group_settings.get(chat_id, {}).get('always_reply', False)

    # Decide whether to respond in a group
    if is_group and not (is_mentioned or always_reply):
        return

    # Remove bot mention in group chats
    if is_mentioned:
        user_message = user_message.replace(f'@{bot_username}', '').strip()

    logger.info(f"Message in {'group' if is_group else 'private'} from user {user_id}: {user_message}")
    
    # Store user message
    store_message(chat_id, user_id, 'user', user_message)
    
    # Generate and store AI response
    ai_response = await generate_response(chat_id, user_id, user_message)
    store_message(chat_id, user_id, 'assistant', ai_response)
    
    logger.info(f"AI response to user {user_id}: {ai_response}")
    await update.message.reply_text(ai_response)

async def set_group_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    if update.effective_chat.type == "private":
        await update.message.reply_text("Settings are only available in group chats.")
        return
    
    # Check if user is an admin
    user = update.effective_user
    chat_member = await update.effective_chat.get_member(user.id)
    
    if not chat_member.status in ['administrator', 'creator']:
        await update.message.reply_text("Only group admins can change settings.")
        return
    
    # Parse settings from command
    try:
        setting = context.args[0]
        value = context.args[1]
        
        if setting == 'always_reply':
            group_settings[chat_id] = {'always_reply': value.lower() == 'true'}
            await update.message.reply_text(f"Always reply set to {value}")
        elif setting == 'max_messages':
            group_settings[chat_id]['max_messages'] = int(value)
            await update.message.reply_text(f"Max messages set to {value}")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /settings always_reply <true/false> or /settings max_messages <number>")

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id in conversations:
        conversations[chat_id].clear()
        await update.message.reply_text("Okh! Let's start with a new conversation.")
    else:
        await update.message.reply_text("No conversation history to forget!")

def main() -> None:
    application = Application.builder().token('7688969617:AAHMogPaXG_9P-g-Gn7POhXrFMEoX1cmYZc').build()

    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('alive', alive))
    application.add_handler(CommandHandler('settings', set_group_settings))
    application.add_handler(CommandHandler('forget', clear_history))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Chatbot Starting...")
    application.run_polling()

if __name__ == '__main__':
    print('Chatbot Starting...')
    try:
        main()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
