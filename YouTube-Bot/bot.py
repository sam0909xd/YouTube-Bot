import telebot
from yt_dlp import YoutubeDL

TOKEN = '7580898976:AAHDF6Wuewx4Mku2TevnI7tWR0gRckm1aKk'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "👋 Hola! Envíame el enlace de YouTube y te descargaré el video en MP4.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if 'youtube.com' in url or 'youtu.be' in url:
        bot.send_message(message.chat.id, "🎥 Descargando tu video, espera un momento...")
        try:
            options = {
                'format': 'mp4',
                'outtmpl': 'video.%(ext)s',
            }
            with YoutubeDL(options) as ydl:
                ydl.download([url])
            video = open('video.mp4', 'rb')
            bot.send_video(message.chat.id, video)
            video.close()
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Error al descargar: {str(e)}")
    else:
        bot.send_message(message.chat.id, "⚠️ Eso no parece un enlace de YouTube.")

bot.polling()
