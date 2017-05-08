import os
import sys
import requests
from json import loads

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

from config import Config as cfg

cf = cfg().load_config_file()['common']
NEWS_API_ENDPOINT = cf['NEWS_API_ENDPOINT']
# Use your own API KEY
NEWS_API_KEY = cf['NEWS_API_KEY']
ARTICALS_API = cf['ARTICALS_API']

CNN = cf['CNN']
DEFAULT_SOURCES = [CNN]

SORT_BY_TOP = cf['SORT_BY_TOP']

CERTIFILE = cf['CERTIFILE']

def buildUrl(end_point=NEWS_API_ENDPOINT, api_name=ARTICALS_API):
    return end_point + api_name

def getNewsFromSource(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
    articles = []
    for source in sources:
        print 'Get news from %s'% source
        payload = {'apiKey' : NEWS_API_KEY,
                   'source' : source,
                   'sortBy' : sortBy}
        response = requests.get(buildUrl(), params=payload, verify=CERTIFILE)
        res_json = loads(response.content)

        # Extract info from response
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):
            # populate news
            for news in res_json['articles']:
                news['source'] = res_json['source']

            articles.extend(res_json['articles'])
    return articles
