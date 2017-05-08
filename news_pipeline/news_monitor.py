# -*- coding: utf-8 -*-

import datetime
import hashlib
import os
import redis
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

from config import Config as cfg
from cloudAMQP_client import CloudAMQPClient
import news_api_client

cf = cfg().load_config_file()['news_pipeline']
REDIS_HOST = cf['REDIS_HOST']
REDIS_PORT = cf['REDIS_PORT']

NEWS_TIME_OUT_IN_SECONDS = cf['NEWS_TIME_OUT_IN_SECONDS']
SLEEP_TIME_IN_SECOUNDS = cf['SLEEP_TIME_IN_SECOUNDS_MONITOR']

# Use your own Cloud AMQP queue
SCRAPE_NEWS_TASK_QUEUE_URL = cf['SCRAPE_NEWS_TASK_QUEUE_URL']
SCRAPE_NEWS_TASK_QUEUE_NAME = cf['SCRAPE_NEWS_TASK_QUEUE_NAME']

NEWS_SOURCES = cf['NEWS_SOURCES']

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
    news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)

    num_of_new_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redis_client.get(news_digest) is None:
            num_of_new_news = num_of_new_news + 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                # format: YYYY-MM-DDTHH:MM:SS in UTC
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            redis_client.set(news_digest, news)
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            cloudAMQP_client.sendMessage(news)

    print "Fetched %d new news." % num_of_new_news

    cloudAMQP_client.sleep(SLEEP_TIME_IN_SECOUNDS)
