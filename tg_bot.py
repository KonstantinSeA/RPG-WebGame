import logging
from telegram.ext import Application, MessageHandler, filters
import sqlite3

BOT_TOKEN = '6556960280:AAHF9q6-1qUlesWwx-M-rxL946oiGl2ceFE'

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
async def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    username = update.message.chat.username
    con = sqlite3.connect('db/blogs.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT login FROM users WHERE login is '{username}'""")
    if len(list(result)) != 0:
        text = 'Телеграмм аккаунт успешно привязан'
    else:
        text = """Вы еще не зарегистрированы.
Пожалуйста зарегистрируйтесь: http://127.0.0.1:8080/register"""
    con.close()
    await update.message.reply_text(text)


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT, echo)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()

