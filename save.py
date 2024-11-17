import telebot
from telebot import types
from yt_dlp import YoutubeDL
import instaloader
from facebook_scraper import get_posts

# Bot token
bot = telebot.TeleBot("7111368882:AAGxK3qehXyY3bYmMN_peUef4qPwGxkx_0o")

# Function to download YouTube video/audio
def download_youtube(link):
    ydl_opts = {
        'format': 'best',  # Use 'bestaudio' for audio only
        'outtmpl': 'video.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    return 'video.mp4'

# Function to download Instagram public content
def download_instagram(link):
    loader = instaloader.Instaloader()
    shortcode = link.split("/")[-2]
    loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode), target=".")
    return f"{shortcode}.jpg"  # Adjust the file extension as needed

# Function to download Facebook video
def download_facebook(link):
    for post in get_posts(link, pages=1):
        video_url = post['video']
        # Code to download the video from the URL goes here
        # For simplicity, we'll return a dummy file path
        return "facebook_video.mp4"

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello! Send me a link, and I'll download the video or audio for you.")

@bot.message_handler(func=lambda message: True)
def handle_links(message):
    link = message.text
    file_path = None

    try:
        if 'youtube.com' in link or 'youtu.be' in link:
            file_path = download_youtube(link)
        elif 'instagram.com' in link:
            file_path = download_instagram(link)
        elif 'facebook.com' in link:
            file_path = download_facebook(link)
        else:
            bot.send_message(message.chat.id, "Sorry, this link is not supported.")
            return

        if file_path:
            with open(file_path, 'rb') as file:
                bot.send_document(message.chat.id, file)

            # Send a follow-up message with an inline keyboard
            markup = types.InlineKeyboardMarkup()
            join_button = types.InlineKeyboardButton("Join Now ❤️‍??", url="https://t.me/creativeydv")
            contact_button = types.InlineKeyboardButton("Contact Owner ??", url="t.me/TMZEROO")
            markup.add(join_button, contact_button)

            bot.send_message(
                message.chat.id,
                "PLEASE JOIN THIS CHANNEL FOR ANY HELP",
                reply_markup=markup
            )

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

bot.polling()
