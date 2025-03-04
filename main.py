import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text("🔌 BOT ACTIVO PAPU 🔥\nManda tu link de YouTube")

async def download_video(update: Update, context):
    url = update.message.text
    cookies = os.getenv("COOKIES")  # 🔑 Llamamos las cookies desde Render

    if not cookies:
        await update.message.reply_text("❌ No hay cookies configuradas")
        return

    with open("cookies.txt", "w") as f:
        f.write(cookies)

    await update.message.reply_text("🎥 Descargando tu video, espera un toque papu...")

    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'best',
        'cookies': 'cookies.txt'
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            await update.message.reply_document(document=open(filename, 'rb'))
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        if os.path.exists("cookies.txt"):
            os.remove("cookies.txt")

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    logger.info("Bot corriendo papu 🔥")
    app.run_polling()

if __name__ == "__main__":
    main()
