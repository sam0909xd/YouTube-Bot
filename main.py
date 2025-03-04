import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from yt_dlp import YoutubeDL

# Configurar logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Token del bot
TOKEN = os.getenv("TOKEN")

# Crear cookies desde Environment Variables
def crear_cookie():
    cookies = os.getenv("COOKIES")
    if cookies:
        with open("cookies.txt", "w") as f:
            f.write(cookies)
        logging.info("✅ Cookies creadas exitosamente")

# Descargar video de YouTube
async def descargar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text
    await update.message.reply_text("🎥 Descargando tu video, espera un toque papu...")

    try:
        crear_cookie()
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'best',
            'cookiefile': 'cookies.txt',  # Aquí le pasamos el archivo de cookies
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        video_title = ydl.extract_info(link, download=False)['title']
        video_file = f"{video_title}.mp4"

        with open(video_file, "rb") as video:
            await update.message.reply_video(video)

        os.remove(video_file)
        os.remove("cookies.txt")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
        logging.error(f"Error al descargar: {e}")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hola papu! Envíame un link de YouTube y te lo descargo gratis 😏.")

# Función principal
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, descargar))

    logging.info("Bot corriendo papu 🔥")
    app.run_polling()

if __name__ == "__main__":
    main()
