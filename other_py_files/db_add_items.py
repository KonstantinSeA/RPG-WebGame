from data import db_session
from data.items import Item


db_session.global_init('../db/blogs.db')
db_sess = db_session.create_session()
item = Item(
    name='Деревянный Нож',
    power=1,
    position='hands',
    about=
    'Старый Игрушечный нож. Выглядит смешно, сложно поверить что этим можно кому-то навредить.'
    ' Сила - 1'
)
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
item = Item(
    name='Новый Деревянный Нож',
    power=2,
    position='hands',
    about='Как старый, только новый. Сила - 2'
)
db_sess.add(item)
db_sess.commit()
item = Item(
    name='Старый Меч Странника',
    power=3,
    position='hands',
    about='Когда-то этим мечом пользовался бродяга, вы никогда не узнаете о нем больше. Сила - 3'
)
db_sess.add(item)
db_sess.commit()
item = Item(
    name='Кожанная Куртка',
    power=3,
    position='body',
    about='Неплохая кожанная куртка. Может не только укрыть от ветра, но и защитить от укуса.'
          ' Сила - 3'
)
db_sess.add(item)
db_sess.commit()
item = Item(
    name='Старый плащ странника',
    power=4,
    position='body',
    about='Когда-то этим плащем пользовался бродяга, вы никогда не узнаете о нем больше. Сила - 4'
)
db_sess.add(item)
db_sess.commit()
item = Item(
    name='Новая Повязка',
    power=2,
    position='head',
    about='Как старая, только новая. Сила - 2'
)
db_sess.add(item)
db_sess.commit()
item = Item(
    name='Старая Шляпа Странника',
    power=3,
    position='head',
    about='Когда-то этой Шляпой пользовался бродяга, вы никогда не узнаете о нем больше. Сила - 3'
)
db_sess.add(item)
db_sess.commit()
item = Item(
    name='Новые Штаны',
    power=2,
    position='legs',
    about='Как старые, только новые. Сила - 2'
)
db_sess.add(item)
db_sess.commit()
item = Item(
    name='Старые штаны странника',
    power=3,
    position='legs',
    about='Когда-то этими штанами пользовался бродяга, вы никогда не узнаете о нем больше. Сила - 3'
)
db_sess.add(item)
db_sess.commit()
