from data import db_session
from data.users import User
from flask_login import current_user


def equip(position, item_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
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
