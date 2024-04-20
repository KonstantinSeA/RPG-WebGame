'''while True:
    print('\n'.join((answer := get_answer())['game_opportunities']))
    line = input()
    request = game_request(line, answer)
    print(request['answer'])
    time.sleep(1)
    after_answer = after_await(request['complete_messange'])
    print(after_answer)'''