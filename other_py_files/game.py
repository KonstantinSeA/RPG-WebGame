from data import db_session
from data.users import User
from flask_login import current_user


def game_request(line):
    pass


def get_answer():
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    if user.energy == 0:
        return None
    if user.level < 5:
        return {
            'location': 'Деревня Ваулли',
            'game_opportunities': ['Отправиться на подработку в Таверну',
                                   'Выполнить Поручение Старосты',
                                   'Отправиться на Охоту'],
            'other_opportunities': ['Узнать о вашем уровне', 'Другое']}
