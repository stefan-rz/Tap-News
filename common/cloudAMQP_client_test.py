import os
import sys

from cloudAMQP_client import CloudAMQPClient
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from config import Config as cfg

cf = cfg().load_config_file()['common']
# Use your own URL
CLOUDAMQP_URL = cf['CLOUDAMQP_URL']

TEST_QUEUE_NAME = 'test'
cf2 = cfg().load_config_file()['news_pipeline']
DEDUPE_NEWS_TASK_QUEUE_URL = cf2['DEDUPE_NEWS_TASK_QUEUE_URL']
DEDUPE_NEWS_TASK_QUEUE_NAME = cf2['DEDUPE_NEWS_TASK_QUEUE_NAME']


def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

    sentMsg = {'test':'demo'}
    client.sendMessage(sentMsg)
    client.sleep(10)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print 'test_basic passed!'

def test_deduperQueue():
    cloudAMQP_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
    sentMsg = {'test': 'demo'}
    cloudAMQP_client.sendMessage(sentMsg)
    cloudAMQP_client.sleep(10)
    receivedMsg = cloudAMQP_client.getMessage()
    assert receivedMsg is not None
    print 'test_deduperQueue passed!'
if __name__ == "__main__":
    test_deduperQueue()
    #test_basic()

