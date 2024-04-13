import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ApplicationBuilder
from telegram.ext import ConversationHandler
import sqlite3

BOT_TOKEN = '6556960280:AAHF9q6-1qUlesWwx-M-rxL946oiGl2ceFE'

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
async def start(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
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
    await update.message.reply_text(text)


async def change_name(update, context):
    await update.message.reply_text('Пожалуйста введите новоё имя персонажа:')
    return 1


async def change_name_response(update, context):
    new_name = update.message.text
    username = update.message.chat.username
    con = sqlite3.connect('db/blogs.db')
    cur = con.cursor()
    cur.execute(f"""UPDATE users SET name = '{new_name}' WHERE login = '{username}'""")
    con.commit()
    con.close()
    await update.message.reply_text("Имя успешно изменено!")
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('change_name', change_name)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_name_response)]
        },
        fallbacks=[MessageHandler(filters.TEXT, change_name_response)]
    )

    application.add_handler(conv_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()

