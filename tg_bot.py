import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ApplicationBuilder
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup
import sqlite3
import schedule
from other_py_files.some_function import equip, shedule_settings
from other_py_files.game import game_request, get_answer, after_await
import time
import random
from data import db_session

BOT_TOKEN = '6556960280:AAHF9q6-1qUlesWwx-M-rxL946oiGl2ceFE'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
db_session.global_init('db/blogs.db')


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    change_name_handler = ConversationHandler(
        entry_points=[CommandHandler('change_name', change_name)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_name_response)]
        },
        fallbacks=[MessageHandler(filters.TEXT, change_name_response)])

    application.add_handler(CommandHandler('start', start))
    application.add_handler(change_name_handler)

    application.add_handler(CommandHandler('inventory', inventory))

    start_game_handler = ConversationHandler(
        entry_points=[CommandHandler('start_game', game_start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, game_response)]
        },
        fallbacks=[MessageHandler(filters.TEXT, game_response)])
    application.add_handler(start_game_handler)

    application.run_polling()


async def start(update, context):
    reply_keyboard = [['/start_game']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    username = update.message.chat.username
    con = sqlite3.connect('db/blogs.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT login, name FROM users WHERE login is '{username}'""")
    result = list(result)
    if len(result) != 0:
        text = f'Здравствуйте, {result[0][1]}!'
    else:
        text = "Вы еще не зарегистрированы. \n" \
               "Пожалуйста зарегистрируйтесь: http://127.0.0.1:8080/register"
    con.close()
    await update.message.reply_text(text, reply_markup=markup)


async def game_start(update, context):
    username = update.message.chat.username
    con = sqlite3.connect('db/blogs.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT id, login, name FROM users WHERE login is '{username}'""")
    user_id = list(result)[0][0]
    con.close()

    # Запрос вариантов действия для пользователя
    answer = get_answer(user_id)
    print(answer)
    reply_keyboard = [[x.split(' - ')[0] for x in ['Отправиться на подработку в Таверну - 30 секун',
                                   'Выполнить Поручение Старосты - 150 секунд',
                                   'Отправиться на Охоту - 90 секунд']],
                      ['Узнать о вашем уровне'],
                      ['/change_name', '/inventory']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # вывод вариантов, print отражает отправку сообщения
    await update.message.reply_text('\n'.join(['Отправиться на подработку в Таверну '
                                               '- 30 секунд',
                                   'Выполнить Поручение Старосты - 150 секунд',
                                   'Отправиться на Охоту - 90 секунд']), reply_markup=markup)
    return 1


async def game_response(update, context):
    username = update.message.chat.username
    con = sqlite3.connect('db/blogs.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT id, login, name FROM users WHERE login is '{username}'""")
    user_id = list(result)[0][0]
    con.close()

    answer = get_answer(user_id)
    reply_keyboard = [[x.split(' - ')[0] for x in ['Отправиться на подработку в Таверну - 30 секуд',
                                   'Выполнить Поручение Старосты - 150 секунд',
                                   'Отправиться на Охоту - 90 секунд']],
                      ['Узнать о вашем уровне'],
                      ['/change_name', '/inventory']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    line = update.message.text
    # создаем запрос к игре
    request_answer = game_request(line, answer, user_id)
    # Проверяем ответ
    if answer == 'No energy':
        await update.message.reply_text('Кажется вы устали...')
        await update.message.reply_text('\n'.join(['Отправиться на подработку в Таверну'
                                                   ' - 30 секунд',
                                   'Выполнить Поручение Старосты - 150 секунд',
                                   'Отправиться на Охоту - 90 секунд']),
                                        reply_markup=markup)
    if request_answer == 'Work in progress':
        await update.message.reply_text('В разработке.', reply_markup=markup)
    # печатаем сообщение ответа
    await update.message.reply_text(request_answer['answer'])
    # ждем определенное в ответе время, лучше писать это асихронно наверное...
    time.sleep(request_answer['await'])
    # запрашиваем результат действия
    after_answer = after_await(request_answer['complete_messange'], user_id)
    # печатаем результат действия
    await update.message.reply_text(after_answer, reply_markup=markup)


async def change_name(update, context):
    reply_keyboard = [['Отмена']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text('Пожалуйста введите новоё имя персонажа:', reply_markup=markup)
    return 1


async def inventory(update, context):
    username = update.message.chat.username
    con = sqlite3.connect('db/blogs.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT id, login, name FROM users WHERE login is '{username}'""")
    user_id = list(result)[0][0]
    con.close()

    answer = get_answer(user_id)
    reply_keyboard = [[x.split(' - ')[0] for x in ['Отправиться на подработку в Таверну - 30 секун',
                                   'Выполнить Поручение Старосты - 150 секунд',
                                   'Отправиться на Охоту - 90 секунд']],
                      ['Узнать о вашем уровне'],
                      ['/change_name', '/inventory']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    username = update.message.chat.username
    con = sqlite3.connect('db/blogs.db')
    cur = con.cursor()
    result = list(cur.execute(f"""SELECT hands, body, legs, head FROM users WHERE login is 
                             '{username}'"""))[0]
    hands = list(cur.execute(f"""SELECT name, about FROM items WHERE id is 
                             '{result[0]}'"""))[0]
    body = list(cur.execute(f"""SELECT name, about FROM items WHERE id is 
                                 '{result[1]}'"""))[0]
    legs = list(cur.execute(f"""SELECT name, about FROM items WHERE id is 
                                 '{result[2]}'"""))[0]
    head = list(cur.execute(f"""SELECT name, about FROM items WHERE id is 
                                 '{result[3]}'"""))[0]
    invent = list(cur.execute(f"""SELECT inventory FROM users WHERE login is 
                                 '{username}'"""))[0][0].split(', ')
    inventory = []
    if len(invent) == 0:
        text_invent = 'У вас больше ничего нет!'
    else:
        for i in range(len(invent)):
            item = list(cur.execute(f"""SELECT name, power FROM items WHERE id is 
                                     '{invent[i]}'"""))
            if item:
                inventory.append(item[0])
        text_invent = 'Также у вас есть следующее снаряжение: '
        for item in inventory:
            text_invent += f'{item[0]}(Сила - {item[1]}), '
    con.close()
    text = "На вас сейчас следующее снаряжение: \n" \
            f"Голова - {head[0]}. {head[1]} \n" \
            f"Тело - {body[0]}. {body[1]} \n" \
            f"Руки - {hands[0]}. {hands[1]} \n" \
            f"Ноги - {legs[0]}. {legs[1]} \n" \
            f"\n" \
            f"{text_invent[:-2]}. Экипировать снаряжение из инвентаря можете на сайте!"

    await update.message.reply_text(text, reply_markup=markup)


async def change_name_response(update, context):
    username = update.message.chat.username
    con = sqlite3.connect('db/blogs.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT id, login, name FROM users WHERE login is '{username}'""")
    user_id = list(result)[0][0]
    con.close()

    answer = get_answer(user_id)
    reply_keyboard = [[x.split(' - ')[0] for x in ['Отправиться на подработку в Таверну - 30 секун',
                                   'Выполнить Поручение Старосты - 150 секунд',
                                   'Отправиться на Охоту - 90 секунд']],
                      ['Узнать о вашем уровне'],
                      ['/change_name', '/inventory']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    new_name = update.message.text
    if new_name != 'Отмена':
        username = update.message.chat.username
        con = sqlite3.connect('db/blogs.db')
        cur = con.cursor()
        cur.execute(f"""UPDATE users SET name = '{new_name}' WHERE login = '{username}'""")
        con.commit()
        con.close()
        await update.message.reply_text("Имя успешно изменено!", reply_markup=markup)
    else:
        await update.message.reply_text("Изменения отменены.", reply_markup=markup)
    return ConversationHandler.END


if __name__ == '__main__':
    main()

