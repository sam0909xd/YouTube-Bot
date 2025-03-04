import yt_dlp
import os

def descargar_video(url):
    cookies = os.getenv("COOKIES")

    options = {
        "outtmpl": "%(title)s.%(ext)s",
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "cookiefile": "cookies.txt",  # Aquí se usan las cookies
        "noprogress": True,
    }

    try:
        with open("cookies.txt", "w") as f:
            f.write(cookies)

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        return "✅ Video descargado correctamente!"
    except Exception as e:
        print(e)
        return "❌ Error al descargar el video!"
