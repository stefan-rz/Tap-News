import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from applogconfig import app_log
app_log.info("Preference list: %s" % str({'key': 'hello', 'demo': 'go' }))