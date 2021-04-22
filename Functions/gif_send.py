import random

import requests
import telegram


def send_gif(update, content):
    query = ' '.join(content.args)
    url = 'https://g.tenor.com/v1/search'
    kwargs = {
        'key': '5XPDWKBEN68J',
        'q': query
    }
    res = requests.get(url, params=kwargs).json()
    if len(res['results']) == 0:
        update.message.reply_text('К сожалению, ничего не нашлось :(')
        return
    res = res['results']
    res = random.choice(res)
    ans = requests.get(res['media'][0]['gif']['url']).content
    try:
        content.bot.send_animation(chat_id=update.message.chat_id, animation=ans)
    except telegram.error.RetryAfter as e:
        update.message.reply_text('Было отправлено слишком много гифок.'
                                  f'Подождите {e.message.split()[-2]} секунд')


def send_some_gifs(update, content):
    try:
        query = ' '.join(content.args[:-1])
        cnt = int(content.args[-1])
        if cnt < 1 or cnt > 5:
            raise ValueError()
    except Exception as e:
        update.message.reply_text('Использование: /gifn <запрос> <число, отделённое '
                                  'пробелом от запроса(количество)>\n'
                                  'Также гифок нельзя взять меньше, чем 1, или больше, чем 5')
        return
    url = 'https://g.tenor.com/v1/search'
    kwargs = {
        'key': '5XPDWKBEN68J',
        'q': query
    }
    res = requests.get(url, params=kwargs).json()
    if len(res['results']) == 0:
        update.message.reply_text('К сожалению, ничего не нашлось :(')
        return
    res = res['results']
    random.shuffle(res)
    try:
        for i in range(cnt):
            ans = requests.get(res[i]['media'][0]['gif']['url']).content
            content.bot.send_animation(chat_id=update.message.chat_id, animation=ans)
    except telegram.error.RetryAfter as e:
        update.message.reply_text('Было отправлено слишком много гифок.'
                                  f'Подождите {e.message.split()[-2]} секунд')
