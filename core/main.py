import os
import logging
import telebot
from gtts import gTTS
from decouple import config

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

if not os.path.exists("voices"):
    os.mkdir("voices")

API_TOKEN = config("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

VOICES_DIR = "voices/"


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Please send me the text you'd like me to convert to speech")


def convert_text_to_speech(text):
    file_path = VOICES_DIR + "generated_speech.mp3"
    tts = gTTS(text=text, lang="en", tld="com")
    tts.save(file_path)
    return file_path


@bot.message_handler(func= lambda message: True)
def text_to_speech(message):
    # logger.info(message.text)
    text = message.text
    try:
        file_path = convert_text_to_speech(text)
        bot.send_voice(chat_id=message.chat.id, reply_to_message_id=message.id, voice=open(file_path, "rb"))
        os.remove(file_path)
    except:
        bot.reply_to(message, "Conversion failed. Please try again")


bot.infinity_polling()
