import os
import sys
import operations
import pyjsonrpc

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

from config import Config as cfg
cf = cfg().load_config_file()['service']
SERVER_HOST = cf['SERVER_HOST']
SERVER_PORT = cf['SERVER_PORT']

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """ Test method """
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print "add is called with %d and %d" % (a, b)
        return a + b

    """ Get news summaries for a user """
    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self, user_id, page_num):
        return operations.getNewsSummariesForUser(user_id, page_num)

    """ Log user news clicks """
    @pyjsonrpc.rpcmethod
    def logNewsClickForUser(self, user_id, news_id, isLikeOn, isDisLikeOn):
        return operations.logNewsClickForUser(user_id, news_id, isLikeOn, isDisLikeOn)

# Threading HTTP Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()
