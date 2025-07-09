import os
import logging
import openai
import asyncio
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
from telegram.constants import ChatAction

# Tokens
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Verificación
if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("⚠️ TELEGRAM_TOKEN y OPENAI_API_KEY deben estar definidos en variables de entorno")

# Prompt del sistema
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
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        reply = respuesta.choices[0].message.content.strip()
    except Exception as e:
        reply = f"⚠️ Error al conectar con OpenAI:\n{e}"

    await update.message.reply_text(reply)

# Run en entorno async activo
async def main():
    logging.basicConfig(level=logging.INFO)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, conversacion))

    print("🤖 Iniciando bot de coaching financiero...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

# Inicia solo si este archivo es el principal
if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except RuntimeError as e:
        # Si Render ya tiene un loop activo, usa este fallback
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()

