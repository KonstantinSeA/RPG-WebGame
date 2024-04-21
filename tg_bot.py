import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ApplicationBuilder
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup
import sqlite3

BOT_TOKEN = '6556960280:AAHF9q6-1qUlesWwx-M-rxL946oiGl2ceFE'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('change_name', change_name)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_name_response)]
        },
        fallbacks=[MessageHandler(filters.TEXT, change_name_response)])

    application.add_handler(CommandHandler('start', start))
    application.add_handler(conv_handler)


    application.run_polling()


async def start(update, context):
    reply_keyboard = [['/change_name']]
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


async def change_name(update, context):
    reply_keyboard = [['Отмена']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text('Пожалуйста введите новоё имя персонажа:', reply_markup=markup)
    return 1


async def change_name_response(update, context):
    reply_keyboard = [['/change_name']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

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

