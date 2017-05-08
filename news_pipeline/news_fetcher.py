# -*- coding: utf-8 -*-

import os
import sys

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

from config import Config as cfg
import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

cf = cfg().load_config_file()['news_pipeline']
# Use your own Cloud AMQP queue
DEDUPE_NEWS_TASK_QUEUE_URL = cf['DEDUPE_NEWS_TASK_QUEUE_URL']
DEDUPE_NEWS_TASK_QUEUE_NAME = cf['DEDUPE_NEWS_TASK_QUEUE_NAME']
SCRAPE_NEWS_TASK_QUEUE_URL = cf['SCRAPE_NEWS_TASK_QUEUE_URL']
SCRAPE_NEWS_TASK_QUEUE_NAME = cf['SCRAPE_NEWS_TASK_QUEUE_NAME']

SLEEP_TIME_IN_SECONDS = cf['SLEEP_TIME_IN_SECONDS_FETCHER']

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not  isinstance(msg, dict):
        print 'message is broken'
        return

    task = msg

    article = Article(task['url'])
    article.download()
    article.parse()

    print article.text

    task['text'] = article.text

    dedupe_news_queue_client.sendMessage(task)

while True:
    # fetch msg from queue
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            # Handle message
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
