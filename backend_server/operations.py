import json
import logging
import os
import pickle
import random
import redis
import sys

from bson.json_util import dumps
from datetime import datetime

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from applogconfig import app_log

import mongodb_client
import news_recommendation_service_client

from cloudAMQP_client import CloudAMQPClient
from config import Config as cfg

cf = cfg().load_config_file()['operations']
REDIS_HOST = cf['REDIS_HOST']
REDIS_PORT = cf['REDIS_PORT']

NEWS_TABLE_NAME = cf['NEWS_TABLE_NAME']
CLICK_LOGS_TABLE_NAME = cf['CLICK_LOGS_TABLE_NAME']

NEWS_LIMIT = cf['NEWS_LIMIT']
NEWS_LIST_BATCH_SIZE = cf['NEWS_LIST_BATCH_SIZE']
USER_NEWS_TIME_OUT_IN_SECONDS = cf['USER_NEWS_TIME_OUT_IN_SECONDS']

# TODO: Use your own queue
LOG_CLICKS_TASK_QUEUE_URL = cf['LOG_CLICKS_TASK_QUEUE_URL']
LOG_CLICKS_TASK_QUEUE_NAME = cf['LOG_CLICKS_TASK_QUEUE_NAME']

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    # The final list of news to be returned.
    sliced_news = []
    print user_id
    if redis_client.get(user_id) is not None:
        app_log.info('redis is not None')
        news_digests = pickle.loads(redis_client.get(user_id))

        # If begin_index is out of range, this will return empty list;
        # If end_index is out of range (begin_index is within the range), this
        # will return all remaining news ids.
        sliced_news_digests = news_digests[begin_index:end_index]
        app_log.info(sliced_news_digests)
        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))
    else:
        db = mongodb_client.get_db()
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digests = map(lambda x:x['digest'], total_news)

        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index:end_index]

    # Get preference for the user
    preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    topPreference = None

    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

    for news in sliced_news:
        # Remove text field to save bandwidth.
        del news['text']
        if news['class'] == topPreference:
            news['reason'] = 'Recommend'
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'

    return json.loads(dumps(sliced_news))

def logNewsClickForUser(user_id, news_id, isLikeToggleOn, isDisLikeToggleOn):
    message = {'userId': user_id, 'newsId': news_id, 'isLikeToggleOn': isLikeToggleOn,
               'isDisLikeToggleOn': isDisLikeToggleOn, 'timestamp': datetime.utcnow()}
    db = mongodb_client.get_db()
    db[CLICK_LOGS_TABLE_NAME].insert(message)
    app_log.info(message)
    print message
    slice_news = db[NEWS_TABLE_NAME].find({'digest': news_id})
    for news in slice_news:
        news['isLkeToggleOn'] = isLikeToggleOn
        news['isDisLikeToggleOn'] = isDisLikeToggleOn
    db['news'].replace_one({'digest': news['digest']}, news, upsert=True)
    app_log.info('%s is inserted successfully into mongodb news table', news)

    # Send log task to machine learning service for prediction
    message = {'userId': user_id, 'newsId': news_id, 'isLikeToggleOn': isLikeToggleOn,
               'isDisLikeToggleOn': isDisLikeToggleOn, 'timestamp': str(datetime.utcnow())}
    cloudAMQP_client.sendMessage(message)


