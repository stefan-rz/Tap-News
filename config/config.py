# -*- coding: utf-8 -*-
import os
import yaml

class Config(object):
    """ Singleton configuration object that ensures consistent and up to date
        setting values.
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
            cls.path = os.path.join(os.path.dirname(__file__), "config.yml")
        return cls.instance


    def load_config_file(self):

        with open(self.path, 'r') as ymlfile:
            settings = yaml.safe_load(ymlfile)
        ymlfile.close
        return settings



