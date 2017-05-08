import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import Config as cfg

def test_read():
    cf = cfg().load_config_file()
    assert 'localhost', cf.operations.REDIS_HOST
    print 'test pass.'

def test_singleton():
    borg = cfg().load_config_file()
    another_borg = cfg().load_config_file()
    print borg is not another_borg
    print borg
    print another_borg
    assert borg, another_borg
    print 'Singleton test pass!'
    cfg()._drop()

if __name__ == "__main__":
    test_read()
    test_singleton()
