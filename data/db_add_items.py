from data import db_session
from data.items import Item


db_session.global_init('../db/blogs.db')
db_sess = db_session.create_session()
item = Item(
    name='Деревянный Нож',
    power=1,
    position='hands',
    about=
    'Старый Игрушечный нож.  Выглядит смешно, сложно поверить что этим можно кому-то навредить. '
    'Сила - 1'
)
db_sess = db_session.create_session()
db_sess.add(item)
db_sess.commit()
item = Item(
    name='Старая Куртка',
    power=2,
    position='body',
    about='Старая выцветшая куртка. В меру удобна, способна укрыть от ветра. Сила - 2'
)
db_sess.add(item)
db_sess.commit()
item = Item(
    name='Потрепанные Штаны',
    power=1,
    position='legs',
    about='Потрепанные Штаны. Лучше чем ничего. Сила - 1'
)
db_sess.add(item)
db_sess.commit()
item = Item(
    name='Повязка',
    power=1,
    position='head',
    about='Повязка на голову. Может укрыть от солнца, наврядли годна для чего-то еще. Сила - 1'
)
db_sess.add(item)
db_sess.commit()