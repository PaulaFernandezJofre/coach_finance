import os
import logging
import openai
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, filters
)
from telegram import ChatAction

# 🔐 Obtén tokens como variables de entorno
TELEGRAM_TOKEN = os.environ['7706288976:AAHRlufto7XhQp9hoWIKaPu8rKCngE2N1XY']
OPENAI_API_KEY = os.environ['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']
openai.api_key = OPENAI_API_KEY

# 🧠 Mensaje del sistema para IA
SYSTEM_PROMPT = """
Eres un mentor financiero experto y motivador, especializado en ayudar a
lograr independencia económica y hacerse millonaria desde cero.
"""

# Comando /start
async def start(update, context):
    usuario = update.effective_user.first_name
    await update.message.reply_text(
        f"Hola {usuario} 💸, soy tu coach financiero personal. "
        "Escríbeme cualquier duda y trabajaremos juntas para que te hagas millonaria 💪"
    )

# Manejo de mensajes
async def conversacion(update, context):
    prompt = update.message.text
    await update.message.chat.send_action(ChatAction.TYPING)
    abierta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    respuesta = abierta.choices[0].message.content
    await update.message.reply_text(respuesta)

# Iniciar bot
async def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, conversacion))
    print("🤖 Bot de coaching financiero corriendo...")
    await app.run_polling()

import asyncio
asyncio.run(main())
