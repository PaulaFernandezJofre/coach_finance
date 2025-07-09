import os
import logging
import openai
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
from telegram.constants import ChatAction

# 🔐 Tokens desde entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Verificación por si olvidaste las variables
if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("⚠️ TELEGRAM_TOKEN y OPENAI_API_KEY deben estar definidos como variables de entorno")

# 🧠 Sistema para OpenAI
SYSTEM_PROMPT = """
Eres un mentor financiero experto y motivador, especializado en ayudar a
lograr independencia económica y hacerse millonaria desde cero.
"""

# Comando /start
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "amiga"
    await update.message.reply_text(
        f"Hola {user} 💸, soy tu coach financiero personal. "
        "Escríbeme cualquier duda y trabajaremos juntas para que te hagas millonaria 💪"
    )

# Manejo de texto
async def conversacion(update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await update.message.chat.send_action(action=ChatAction.TYPING)
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",  # cambia a gpt-3.5-turbo si es necesario
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        reply = respuesta.choices[0].message.content.strip()
    except Exception as e:
        reply = f"⚠️ Error en la respuesta de OpenAI: {e}"

    await update.message.reply_text(reply)

# Función principal
async def run_bot():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, conversacion))
    print("🤖 Bot financiero corriendo en Render...")
    await app.run_polling()

# 👇 Esta parte evita usar asyncio.run o loop.run_until_complete
import asyncio

if __name__ == "__main__":
    asyncio.get_event_loop().create_task(run_bot())
    asyncio.get_event_loop().run_forever()
