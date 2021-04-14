import telebot
from telebot import types
from config import token
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import lxml

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def command_help(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('случайная статья wiki 🌐')
    btn2 = types.KeyboardButton('случайная цитата')
    keyboard.add(btn, btn2)

    bot.send_message(message.chat.id,
                     'Нажатие на кнопку присылает случайную статью. Ввод текста поиск совпадений в wiki',
                     reply_markup=keyboard)


def get_page(url, params=None):
    ua = UserAgent().chrome
    r = requests.get(url, headers={'User-Agent': ua}, params=params)
    return r


def get_random_wiki_page():
    """
    возвращает ссылку на случайную статью с википедии
    :return:
    """
    url = 'https://ru.wikipedia.org'
    wiki_page = get_page(url)

    soup = BeautifulSoup(wiki_page.text, 'lxml')
    get_random_link = soup.find('li', id='n-randompage').find('a').get('href')
    random_page_link = url + get_random_link
    page = get_page(random_page_link)
    the_page = page.url
    # soup = BeautifulSoup(r.text, 'lxml')
    # get_header = soup.find('h1', id='firstHeading').get_text().strip()
    return the_page


def get_search_page(word):
    clear_word = word.replace(' ', '_')
    url = 'https://ru.wikipedia.org/wiki/' + word
    page = get_page(url)
    the_page = page.url
    return the_page


def random_quote():
    url = 'https://quote-citation.com/random'
    quote_page = get_page(url)
    soup = BeautifulSoup(quote_page.text, 'lxml')
    text = soup.find('div', class_='quote-text').find('p').get_text().strip()
    author = soup.find('p', class_='source').get_text().strip()
    return text, author


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text == 'случайная статья wiki 🌐':
        link = get_random_wiki_page()
        bot.send_message(message.chat.id, link)
    elif message.text == 'случайная цитата':
        text, author = random_quote()
        bot.send_message(message.chat.id, f'{text}\n {author}')

    else:
        word = message.text
        link = get_search_page(word)
        bot.send_message(message.chat.id, link)


bot.polling()
