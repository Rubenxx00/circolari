import schedule
import time
import secret
import telegram
from data import Data
from telegram import Bot
from reader import get_latest_url, get_news_in_page
import logging
import logging.config

client = Bot(secret.TOKEN)
CHAT_ID = secret.CHAT

data = Data.load()

logging.config.dictConfig({
    "version": 1,
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": "app.log",
            "mode": "a"
        }
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s [PID %(process)d] [%(levelname)s] %(message)s"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "file"
        ]
    }
})
logger = logging.getLogger()


def get_updates(data: Data):
    try:
        # init
        if data.latest_url == '':
            data.latest_url = get_latest_url()
        queue = get_news_in_page(data.latest_url, until=data.latest_id)
        logger.info("Found %d news in cached page", len(queue))
        # check if new month
        if get_latest_url() != data.latest_url:
            logger.info('Found new month...')
            data.latest_url = get_latest_url()
            queue.extend(get_news_in_page(data.latest_url))
        if len(queue) > 0:
            logger.debug("Found %d new updates", len(queue))
            queue = queue[::-1]
            data.latest_id = queue[-1].id
            if data.latest_id != max([x.id for x in queue]):
                logger.warning("Post order is strange: %s",
                               ', '.join(str(q.id) for q in queue))
        return queue
    except Exception as e:
        logger.error(e, exc_info=True)


def task(data: Data):
    logger.info('Task started')
    updates = get_updates(data)
    for u in updates:
        try:
            text = (f'Circolare n. {u.id} del {u.date}\n\n'
                    + f'<b>{u.title}</b>\n\n'
                    + f'➡️ {u.link}')
            if u.attachment != None:
                text += f'\n\n🔗<a href="{u.attachment}">Allegato</a>'
            try:
                client.send_message(
                    CHAT_ID, text, parse_mode=telegram.ParseMode.HTML)
                time.sleep(1)
            except TimeoutError:  # retry
                logger.debug('Retrying sending number %d', u.id)
                client.send_message(
                    CHAT_ID, text, parse_mode=telegram.ParseMode.HTML)
        except Exception as e:
            logger.error(e, exc_info=True)


task(data)

schedule.every(15).minutes.do(task)

while True:
    schedule.run_pending()
    time.sleep(60)
