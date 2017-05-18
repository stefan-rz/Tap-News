# -*- coding: utf-8 -*-
import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '.', 'config'))
from config import Config as cfg

cf = cfg().load_config_file()['logging']
# Set the message format

format = logging.Formatter("%(levelname)s %(name)-10s  %(asctime)s %(message)s")
# Create a handler that prints ERROR level messages to stderr
err_hand = logging.StreamHandler(sys.stderr)
err_hand.setLevel(logging.ERROR)
err_hand.setFormatter(format)
# Create a handler that prints messages to a file
applog_hand = logging.FileHandler(cf['handler_applog']['args'])
applog_hand.setFormatter(format)
# Create a top-level logger called 'app'
app_log = logging.getLogger(cf['loggers']['keys'][1])
app_log.setLevel(logging.INFO)
app_log.addHandler(applog_hand)
app_log.addHandler(err_hand)
