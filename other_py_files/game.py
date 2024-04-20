from data import db_session
from data.users import User
import random
from other_py_files.some_function import add_item, check_item, add_xp


db_session.global_init('db/blogs.db')
db_sess = db_session.create_session()
current_user = db_sess.query(User).get(1)


def game_request(line, answer):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    level = 4
    if user.energy > 0:
        if answer['location'] == 'Деревня Ваулли':
            if line == 'Отправиться на подработку в Таверну':
                return {'answer': 'Вы отправляетесь в местную таверну...'
                                  '\nХозяин таверны дает вам несколько поручений.',
                        'await': 30,
                        'complete_messange': 'complete_common_work_1'}
            elif line == 'Выполнить Поручение Старосты':
                if random.choice([*[True] * (10 - 4 + user.level), *[False] * (4 - user.level)]):
                    return {'answer': 'Вы отправляетесь к старосте деревни...'
                                      '\nУ старосты найдется несколько поручений для вас...',
                            'await': 150,
                            'complete_messange': 'complete_long_work_1'}
                return {'answer': 'Вы отправляетесь к старосте деревни...'
                                  '\nУ старосты найдется несколько поручений для вас...',
                        'await': 75,
                        'complete_messange': 'lose_long_work_1'}
            elif line == 'Отправиться на Охоту':
                if random.choice([*[True] * (20 - 8 + 2 * (level - 4)),
                                  *[False] * (8 - 2 * (level - 4))]):
                    return {'answer': 'Вместе с местными вы отпраляетесь на Охоту...'
                                      '\nСегодня все идет неплохо...',
                            'await': 90,
                            'complete_messange': 'complete_common_fight_1'}
                return {'answer': 'Вместе с местными вы отпраляетесь на Охоту...'
                                  '\nКажется сегодня вы практически никого не встретите...',
                        'await': 45,
                        'complete_messange': 'lose_common_fight_1'}
            elif line == 'Узнать о вашем уровне':
                return {'answer': f'Ваш Уровень: {user.level}'
                                  f'До повышения: {500 - user.xp}',
                        'await': 0,
                        'complete_messange': 'no messange'}
            elif line == 'Другое':
                return {'answer': 'Больше Возможностей доступны на сайте:',
                        'await': 0,
                        'complete_messange': 'no messange'}
        return 'Work in progress'
    return 'No energy'


def get_answer():
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    if user.energy <= 0:
        return None
    if user.level < 5:
        return {
            'location': 'Деревня Ваулли',
            'fon_image': 'Village.jpg',
            'game_opportunities': ['Отправиться на подработку в Таверну - 30 секунд',
                                   'Выполнить Поручение Старосты - 150 секунд',
                                   'Отправиться на Охоту - 90 секунд'],
            'other_opportunities': ['Узнать о вашем уровне', 'Другое']}


def after_await(complete_messange):
    if complete_messange == 'complete_common_work_1':
        if random.choice([*[True] * 5, *[False] * 95]) and not check_item(6):
            add_item(6)
            add_xp(50)
            return 'Ваша работа Окончена! Вам очень повезло! ' \
                   'Один из постояльцев дарит вам свой меч.' \
                   '\nПолучен Предмет: Старый меч странника' \
                   '\nПолучен Опыт: 50'
        if random.choice([*[True] * 15, *[False] * 85]) and not check_item(5):
            add_item(5)
            add_xp(50)
            return 'Ваша работа Окончена! Вам повезло! ' \
                   'Раздобрившись Хозяин таверны дарит вам новый нож.' \
                   '\nПолучен Предмет: Новый Деревянный Нож' \
                   '\nПолучен Опыт: 50'
        add_xp(50)
        return 'Ваша работа Окончена!' \
               '\nПолучен Опыт: 50'
    elif complete_messange == 'complete_long_work_1':
        if random.choice([*[True] * 5, *[False] * 95]) and not check_item(8):
            add_item(8)
            add_xp(100)
            return 'Вы выполнили поручение! Вам очень повезло! ' \
                   'В награду староста дарит вам свой старый плащ' \
                   '\nПолучен Предмет: Старый плащ странника' \
                   '\nПолучен Опыт: 100'
        if random.choice([*[True] * 15, *[False] * 85]) and not check_item(7):
            add_item(7)
            add_xp(100)
            return 'Вы выполнили поручение! Вам повезло! ' \
                   'Выполняя поручение вы нашли новую куртку' \
                   '\nПолучен Предмет: Кожанная Куртка' \
                   '\nПолучен Опыт: 100'
        add_xp(100)
        return 'Вы выполнили поручение!' \
               '\nПолучен Опыт: 100'
    elif complete_messange == 'lose_long_work_1':
        add_xp(10)
        return 'Вам не удалось выполнить поручение...' \
               '\nПолучен Опыт: 10'
    elif complete_messange == 'complete_common_fight_1':
        if random.choice([*[True] * 5, *[False] * 95]) and not check_item(12):
            add_item(12)
            add_xp(100)
            return 'Сегодня Охота удалась! Вам очень повезло! ' \
                   'Охотники Дарят вам подарок!' \
                   '\nПолучен Предмет: Старые штаны странника' \
                   '\nПолучен Опыт: 100'
        if random.choice([*[True] * 5, *[False] * 95]) and not check_item(10):
            add_item(10)
            add_xp(100)
            return 'Сегодня Охота удалась! Вам очень повезло! ' \
                   'Охотники Дарят вам подарок!' \
                   '\nПолучен Предмет: Старая Шляпа Странника' \
                   '\nПолучен Опыт: 100'
        if random.choice([*[True] * 15, *[False] * 85]) and not check_item(11):
            add_item(11)
            add_xp(100)
            return 'Сегодня Охота удалась! Вам повезло! ' \
                   'Вы обмениваете добычу на новые штаны' \
                   '\nПолучен Предмет: Новые Штаны' \
                   '\nПолучен Опыт: 100'
        if random.choice([*[True] * 15, *[False] * 85]) and not check_item(9):
            add_item(9)
            add_xp(100)
            return 'Сегодня Охота удалась! Вам повезло! ' \
                   'Вы обмениваете добычу на новую повязку' \
                   '\nПолучен Предмет: Новая Повязка' \
                   '\nПолучен Опыт: 100'
        add_xp(100)
        return 'Сегодня Охота удалась!' \
               '\nПолучен Опыт: 100'
    elif complete_messange == 'lose_common_fight_1':
        add_xp(5)
        return 'Сегодня охота не удалась...' \
               '\nПолучен Опыт: 5'
