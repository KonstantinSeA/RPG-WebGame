from data import db_session
from data.users import User
import schedule


def equip(position, item_id, current_user):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user)
    if position == 'head':
        old = user.head
        user.head = item_id
        inventory = user.inventory.split(', ')
        inventory.pop(inventory.index(str(item_id)))
        inventory.append(str(old))
        user.inventory = ', '.join(inventory)
    elif position == 'body':
        old = user.body
        user.body = item_id
        inventory = user.inventory.split(', ')
        inventory.pop(inventory.index(str(item_id)))
        inventory.append(str(old))
        user.inventory = ', '.join(inventory)
    elif position == 'legs':
        old = user.legs
        user.legs = item_id
        inventory = user.inventory.split(', ')
        inventory.pop(inventory.index(str(item_id)))
        inventory.append(str(old))
        user.inventory = ', '.join(inventory)
    else:
        old = user.hands
        user.hands = item_id
        inventory = user.inventory.split(', ')
        inventory.pop(inventory.index(str(item_id)))
        inventory.append(str(old))
        user.inventory = ', '.join(inventory)
    db_sess.commit()


def add_item(item_id, current_user):
    if not check_item(item_id, current_user):
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user)
        user.inventory += ', ' + str(item_id)
        db_sess.commit()


def check_item(item_id, current_user):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user)
    inv = user.inventory.split(', ')
    ans = str(item_id) in user.inventory.split(', ')
    return str(item_id) in user.inventory.split(', ')


def add_xp(xp, current_user):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user)
    user.xp += xp
    if user.level < 5:
        if user.xp >= 500:
            user.xp %= 500
            user.level += 1
    db_sess.commit()


def energy_low(energy, current_user):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user)
    user.energy -= energy
    db_sess.commit()


def shedule_settings():
    schedule.every().day().at('4:00').do(energy_back())


def energy_back():
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        user.energy = 10
    db_sess.commit()
