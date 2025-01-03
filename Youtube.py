import telebot
import os
from yt_dlp import YoutubeDL

# Bot tokenini oling (muhit o'zgaruvchisidan yoki statik ravishda)
BOT_TOKEN = os.getenv("BOT_TOKEN", "7626491002:AAHVI9QxB30ejGhqYFr_ZRcbMGIUa3eh9Ig")
bot = telebot.TeleBot(BOT_TOKEN)

# YouTube linkdan video yuklab olish funksiyasi
def download_video(url):
    options = {
        'format': 'best',
        'outtmpl': 'video.mp4',
    }
    with YoutubeDL(options) as ydl:
        ydl.download([url])
    return 'video.mp4'

# Start komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Menga YouTube video havolasini yuboring.")

# Video yuklab olish
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        bot.reply_to(message, "Videoni yuklab olmoqdaman, kuting...")
        try:
            video_path = download_video(url)
            with open(video_path, 'rb') as video:
                bot.send_video(message.chat.id, video)
            if os.path.exists(video_path):
                os.remove(video_path)  # Faylni o‘chirish
        except Exception as e:
            bot.reply_to(message, f"Xato yuz berdi: {str(e)}")
    else:
        bot.reply_to(message, "Bu YouTube havolasi emas. To‘g‘ri havola yuboring.")

# Botni ishga tushirish
bot.polling()
