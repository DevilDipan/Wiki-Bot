import time
from telebot import TeleBot, types
import wikipedia

bot_token = ''  # Paste the Token API
bot = TeleBot(token=bot_token)
error = 'Sorry, Processing Failed'
word = " for the word..."


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, text='Greetings! Welcome, I am WikiBot.', reply_markup=main_keyboard())


@bot.message_handler(commands=['extra'])
def send_welcome(message):
    text = '/purpose - shows the purpose Why I made this, \n' \
           '/dev - provides information about me.'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=main_keyboard())


@bot.message_handler(commands=['purpose'])
def purpose(message):
    text = 'This is a very simple bot, made with the purpose of helping people learn more about bots.'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=main_keyboard())


@bot.message_handler(commands=['dev'])
def dev(message):
    text = 'This is made with ❤ by @themagicalmammal.\nIf you require assistance or want me to update the bot, ' \
           'Please feel free to contact me. '
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=main_keyboard())


@bot.message_handler(commands=['help'])
def aid(message):
    text = '/def - fetches definition of the word you typed, \n' \
           '/title - fetches a bunch of possible titles for the word you send, \n' \
           '/url - gives the url for the wiki page of the word you typed, \n' \
           '/random - fetches a random title from the wiki page.'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=main_keyboard())


@bot.message_handler(commands=['title'])
def title(message):
    title_msg = bot.reply_to(message, "Title" + word)
    bot.register_next_step_handler(title_msg, process_title)


def process_title(message):
    # noinspection PyBroadException
    try:
        title_message = str(message.text)
        title_result = wikipedia.search(title_message, results=4)
        for i in title_result:
            bot.send_message(chat_id=message.chat.id, text=i, reply_markup=main_keyboard())
    except Exception:
        bot.send_message(chat_id=message.chat.id, text=error, reply_markup=main_keyboard())


@bot.message_handler(commands=['url'])
def url(message):
    url_msg = bot.reply_to(message, "URL" + word)
    bot.register_next_step_handler(url_msg, process_url)


def process_url(message):
    # noinspection PyBroadException
    try:
        url_message = str(message.text)
        url_string = wikipedia.page(url_message)
        url_result = str(url_string.url)
        bot.send_message(chat_id=message.chat.id, text=url_result, reply_markup=main_keyboard())
    except Exception:
        bot.send_message(chat_id=message.chat.id, text=error, reply_markup=main_keyboard())


@bot.message_handler(commands=['random'])
def random(message):
    # noinspection PyBroadException
    try:
        random_title = str(wikipedia.random(pages=1))
        bot.send_message(chat_id=message.chat.id, text=random_title, reply_markup=main_keyboard())
    except Exception:
        bot.send_message(chat_id=message.chat.id, text=error, reply_markup=main_keyboard())


@bot.message_handler(commands=['def'])
def definition(message):
    def_msg = bot.reply_to(message, "Definition" + word)
    bot.register_next_step_handler(def_msg, process_definition)


def process_definition(message):
    try:
        def_message = str(message.text)
        def_string = str(wikipedia.summary(def_message, sentences=20, auto_suggest=True, redirect=True))
        bot.send_message(chat_id=message.chat.id, text=def_string, reply_markup=main_keyboard())
    except Exception as c:
        bot.send_message(chat_id=message.chat.id, text=c, reply_markup=definition(message))


def main_keyboard():
    time.sleep(2)
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    texts = ['/def', '/title', '/url', '/random', '/help', '/extra']
    buttons = []
    for text in texts:
        button = types.KeyboardButton(text)
        buttons.append(button)
    markup.add(*buttons)
    return markup


while True:
    # noinspection PyBroadException
    try:
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.polling()
    except Exception:
        time.sleep(5)
