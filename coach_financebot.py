import os
import logging
import openai
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, filters
)
from telegram.constants import ChatAction

# 🔐 Leer tokens desde variables de entorno
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# 🧠 Prompt del sistema
SYSTEM_PROMPT = """
Eres un mentor financiero experto y motivador, especializado en ayudar a
lograr independencia económica y hacerse millonaria desde cero.
"""

# Comando /start
async def start(update, context):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"Hola {user} 💸, soy tu coach financiero personal. "
        "Escríbeme cualquier duda y trabajaremos juntas para que te hagas millonaria 💪"
    )

# Conversación principal
async def conversacion(update, context):
    user_input = update.message.text
    await update.message.chat.send_action(action=ChatAction.TYPING)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # puedes cambiar a "gpt-3.5-turbo" si no tienes acceso a GPT-4
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ Ocurrió un error con OpenAI: {e}"

    await update.message.reply_text(reply)

# Ejecutar el bot
async def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, conversacion))

    print("🤖 Bot de coaching financiero corriendo...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
