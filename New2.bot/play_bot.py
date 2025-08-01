import telebot
import os   
import random
import json

TOKEN = '8467133729:AAH87WsAPchzRTJWmvXBf6SC3JmmMu2Z3H0'  
bot = telebot.TeleBot(TOKEN)
if not os.path.exists("Alicho"):
    os.makedirs("Alicho")
@bot.message_handler(content_types=['photo', 'document'])
def handle_files(message):
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        filename = f"photo_{message.chat.id}_{file_info.file_unique_id}.jpg"
    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        filename = message.document.file_name
    file_path = os.path.join("Alicho", filename)
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    bot.send_message(message.chat.id, "Файл сохранен!")

user_guesses = {}

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Я бот.  /guess для число от 1 до 100: /word для изучения english.")
    new_game(message)

@bot.message_handler(commands=['guess'])
def new_game(message):
    number = random.randint(1, 100)
    user_guesses[message.chat.id] = number
    bot.send_message(message.chat.id, " число от 1 до 100. угадай!")

@bot.message_handler(func=lambda m: m.chat.id in user_guesses and m.text.isdigit())
def handle_guess(message):
    guess = int(message.text)
    target = user_guesses[message.chat.id]

    if guess < target:
        bot.send_message(message.chat.id, " больше.")
    elif guess > target:
        bot.send_message(message.chat.id, " меньше.")
    else:
        bot.send_message(message.chat.id, " Ты угадал ")
        del user_guesses[message.chat.id]
words = {
    "apple": "яблоко",
    "dog": "собака",
    "sun": "солнце",
    "house": "дом",
    "book": "книга"
}
user_stats = {}
@bot.message_handler(commands=['word'])
def send_random_word(message):
    word = random.choice(list(words.keys()))
    user_stats[message.chat.id] = word
    bot.send_message(message.chat.id, f"Как переводится слово: *{word}*?", parse_mode='Markdown')
@bot.message_handler(func=lambda m: m.chat.id in user_stats)
def check_translation(message):
    word = user_stats[message.chat.id]
    correct_translation = words[word].lower()
    user_answer = message.text.strip().lower()
    if user_answer == correct_translation:
        bot.send_message(message.chat.id, " Правильно!")
    else:
        bot.send_message(message.chat.id, f" Неправильно. Правильно: *{correct_translation}*", parse_mode='Markdown')
    del user_stats[message.chat.id]
bot.polling(none_stop=True)