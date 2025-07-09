import os
import logging
import openai
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
from telegram.constants import ChatAction

# 🔐 Leer tokens desde variables de entorno
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# 🔍 Validar que las claves estén configuradas
if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise EnvironmentError("❌ TELEGRAM_TOKEN o OPENAI_API_KEY no están definidos en variables de entorno.")

openai.api_key = OPENAI_API_KEY

# 🧠 Prompt del sistema
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

# Conversación principal
async def conversacion(update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await update.message.chat.send_action(action=ChatAction.TYPING)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Cambia a "gpt-3.5-turbo" si usas el plan gratuito
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"⚠️ Ocurrió un error con OpenAI:\n{e}"

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
    import sys

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
