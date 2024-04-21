# Необходимо запустить БД и заявить пользователя с которым работаем
db_session.global_init('db/blogs.db')
user_id = 1
# Цикл отражает состояние ожидание ответа
while True:
    # Запрос вариантов действия для пользователя
    answer = get_answer(user_id)
    # проверка ответа
    if answer == 'No energy':
        print('Кажется вы устали...')
        continue
    # вывод вариантов, print отражает отправку сообщения
    print('\n'.join(answer['game_opportunities']))
    # считываем ответ пользователя
    line = input()
    # создаем запрос к игре
    request_answer = game_request(line, answer, 1)
    # Проверяем ответ
    if answer == 'No energy':
        print('Кажется вы устали...')
        continue
    if request_answer == 'Work in progress':
        print('В разработке.')
        continue
    # печатаем сообщение ответа
    print(request_answer['answer'])
    # ждем определенное в ответе время, лучше писать это асихронно наверное...
    time.sleep(request_answer['await'])
    # запрашиваем результат действия
    after_answer = after_await(request_answer['complete_messange'], 1)
    # печатаем результат действия
    print(after_answer)
