import telebot
from telebot import types

bot = telebot.TeleBot("1644078195:AAFRVYY9fzyYXs45hVJcVXZnp-cH8TznesY")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start',
                     reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['open_keyboard'])
def open_keyboard(message):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="yes", callback_data="yes")
    btn2 = types.InlineKeyboardButton(text="no", callback_data="no")
    keyboard.add(btn1, btn2)
    bot.send_message(message.chat.id, 'you are a user', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == "yes":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("yes")
        btn2 = types.KeyboardButton("no")
        keyboard.add(btn1, btn2)
        bot.send_message(call.message.chat.id, "you are a programmer?", reply_markup=keyboard)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "you are not a user ???",
                         reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == "yes":
        bot.send_message(message.chat.id, "you are a programmer",
                         reply_markup=types.ReplyKeyboardRemove())
        return
    elif message.text == "no":
        bot.send_message(message.chat.id, "you are not a programmer",
                         reply_markup=types.ReplyKeyboardRemove())
        return
    bot.send_message(message.chat.id, message.text + "!",
                     reply_markup=types.ReplyKeyboardRemove())


bot.polling()
