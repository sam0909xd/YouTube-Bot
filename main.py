from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from descargar import descargar_video
import os
import logging

# Configurar logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Hola papurri! Mándame un link de YouTube y te devuelvo el video 🎥🔥.")

def descargar(update: Update, context: CallbackContext):
    url = update.message.text
    chat_id = update.message.chat_id

    if "youtube.com" in url or "youtu.be" in url:
        update.message.reply_text("🎥 Descargando tu video, espera un ratito...")

        respuesta = descargar_video(url)

        if respuesta == "✅ Video descargado correctamente!":
            archivo = obtener_archivo()
            context.bot.send_video(chat_id=chat_id, video=open(archivo, "rb"))
            os.remove(archivo)
            update.message.reply_text("✅ Aquí está tu video papu 🔥🔥")
        else:
            update.message.reply_text("❌ No se pudo descargar el video.")
    else:
        update.message.reply_text("❌ Solo acepto links de YouTube crack 😏.")

def obtener_archivo():
    for archivo in os.listdir():
        if archivo.endswith(".mp4") or archivo.endswith(".webm") or archivo.endswith(".m4a"):
            return archivo
    return None

def main():
    bot = Bot(token=TOKEN)
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, descargar))

    updater.start_polling()
    logger.info("✅ Bot encendido 🔥")
    updater.idle()

if __name__ == "__main__":
    main()
