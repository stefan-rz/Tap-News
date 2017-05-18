import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

import mongodb_client
import news_topic_modeling_service_client
from applogconfig import app_log

if __name__ == '__main__':
    db = mongodb_client.get_db()
    cursor = db['news'].find({})
    count = 0
    for news in cursor:
        count += 1
        print count
        if 'class' not in news:
            app_log.info('Populating classes...')
            title = news['title']
            topic = news_topic_modeling_service_client.classify(title)
            news['class'] = topic
            db['news'].replace_one({'digest': news['digest']}, news, upsert=True)
        if 'isLikeToggleOn' in news:
            app_log.info('Populating isLikeToggleOn...')
            news['isLikeToggleOn'] = False
            db['news'].replace_one({'digest': news['digest']}, news, upsert=True)
        if 'isDisLikeToggleOn'  in news:
            app_log.info('Populating isLikeToggleOn...')
            news['isDisLikeToggleOn'] = False
            db['news'].replace_one({'digest': news['digest']}, news, upsert=True)


