import logging
import os
import sys
import pyjsonrpc
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

from applogconfig import app_log

from config import Config as cfg
cf = cfg().load_config_file()['common']
URL = cf['news_recommendation_service_client']['URL']


client = pyjsonrpc.HttpClient(url=URL)

def getPreferenceForUser(userId):
    preference = client.call('getPreferenceForUser', userId)
    app_log.info("Preference list: %s" % str(preference))
    return preference
