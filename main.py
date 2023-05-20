from telebot import TeleBot, types
import os
from tgtoken import *

bot = TeleBot(token)

commands = [
        {"command": "help", "description": "Commands list"},
        {"command": "info", "description": "Why am I needed?"},
        {"command": "send_sound", "description": "Send sound"},
        {"command": "author", "description": "Info about author"},
    ]

packs = os.listdir("Packs")

@bot.message_handler(commands=['start', 'help'])
def handle_start_command(message):
    chat_id = message.chat.id
    text = "Hello! This is SoundPack bot.\n"
    
    for cmd in commands:
        text += "\n/" + cmd['command'] + " − " + cmd['description']

    bot.send_message(chat_id, text=text)

@bot.message_handler(commands=['info'])
def handle_author_command(message):
    chat_id = message.chat.id
    with open('info.txt', 'r') as file:
        text = file.read()
    bot.send_message(chat_id, text=text)

@bot.message_handler(commands=['author'])
def handle_author_command(message):
    chat_id = message.chat.id
    author = "Sergey Krivtsov"
    github = "alwaysmeow"
    email = "krivtsovsergey2003@gmail.com"
    bot.send_message(chat_id, text = f"Author: {author}\n\nGitHub: {github}\n\nemail: {email}\n\nThank you for your attention!")

@bot.message_handler(commands=['send_sound'])
def handle_send_voice_command(message):
    chat_id = message.chat.id
    packsMarkup = types.InlineKeyboardMarkup()
    for pack in packs:
        packsMarkup.add(types.InlineKeyboardButton(pack, callback_data = "pack:" + pack))
    bot.send_message(chat_id, "Choose pack:", reply_markup=packsMarkup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('pack:'))
def handle_pack_button_click(call):
    chat_id = call.message.chat.id
    pack = call.data.split(':')[1]
    if pack == "?":
        packsMarkup = types.InlineKeyboardMarkup()
        for pack in packs:
            packsMarkup.add(types.InlineKeyboardButton(pack, callback_data = "pack:" + pack))
        bot.edit_message_text("Choose pack:", chat_id, message_id = call.message.message_id, reply_markup=packsMarkup)
    else:
        path = "Packs\\" + pack
        sounds = os.listdir(path)
        soundsMarkup = types.InlineKeyboardMarkup()
        for sound in sounds:
            soundsMarkup.add(types.InlineKeyboardButton(sound, callback_data = "sound:" + pack + "\\" + sound))
        soundsMarkup.add(types.InlineKeyboardButton("Choose another pack", callback_data="pack:?"))
        bot.edit_message_text("Choose sound:", chat_id, message_id = call.message.message_id, reply_markup=soundsMarkup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('sound:'))
def handle_sound_button_click(call):
    chat_id = call.message.chat.id
    sound = call.data.split(':')[1]
    bot.send_photo(chat_id, photo=open("Packs\\" + sound + "\\pic.png", "rb"))
    bot.send_voice(chat_id, voice=open("Packs\\" + sound + "\\sound.mp3", "rb"))

bot.polling()