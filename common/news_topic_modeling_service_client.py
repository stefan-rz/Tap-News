import os
import sys
import pyjsonrpc

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

from config import Config as cfg
cf = cfg().load_config_file()['common']
URL = cf['news_topic_modeling_service_client']['URL']

client = pyjsonrpc.HttpClient(url=URL)

def classify(text):
    topic = client.call('classify', text)
    print "Topic: %s" % str(topic)
    return topic
