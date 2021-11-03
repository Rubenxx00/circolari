import schedule
import time

import telegram
from data import Data
from telegram import Bot
from reader import get_latest_url, get_news_in_page

TOKEN = ''
CHAT_ID = ''

client = Bot(TOKEN)

data = Data.load()

def get_updates():
    # init
    if data.latest_url == '':
        data.latest_url = get_latest_url()
    queue = get_news_in_page(data.latest_url, until=data.latest_id)
    # check if new month
    if get_latest_url != data.latest_url:
        data.latest_url = get_latest_url()
        queue.extend(get_news_in_page(data.latest_url))
    if len(queue) > 0:
        queue = queue[::-1]
        data.latest_id = queue[0].id
    return queue

def task(data: Data):
    updates = get_updates()
    for u in updates:
        text = (f'Circolare n. {u.id} del {u.date}\n\n'
                + f'<b>{u.title}</b>\n\n'
                + f'➡️ {u.link}')
        if u.attachment != None:
            text += f'\n\n🔗<a href="{u.attachment}">Allegato</a>'
        client.send_message(CHAT_ID, text, parse_mode=telegram.ParseMode.HTML)

task(data)

schedule.every(1).hour.do(task)

while True:
    schedule.run_pending()
    time.sleep(60)
