from scrapy import crawler

from stem import Signal
from stem.control import Controller
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from stem.util.log import get_logger




# Number of requests sent during the current tor identity



def new_tor_identity():
    with Controller.from_port(port=9051) as controller:
        # authenticate with the tor password
        file = open('password.txt')
        passwrod = file.readline()
        controller.authenticate(password=passwrod)

        # Change tor identity
        controller.signal(Signal.NEWNYM)


class ProxyMiddleware(HttpProxyMiddleware):

    def __init__(self, *args, **kwargs):
        super(ProxyMiddleware, self).__init__()
        self.NUM_SENT_REQUESTS = 0





    def process_response(self, request, response, spider):

        # Get a new identity depending on the response
        if response.status != 200:
            new_tor_identity()
            self.NUM_SENT_REQUESTS = 0
            return request

        return response

    def process_request(self, request, spider):

        # Set the Proxy
        # A new identity for each N requests request


        if self.NUM_SENT_REQUESTS >= spider.REQUESTS_PER_SAME_TOR_IDENTITY :
            self.NUM_SENT_REQUESTS = 0
            new_tor_identity()

        self.NUM_SENT_REQUESTS += 1

        # add a proxy for the response
        request.meta['proxy'] = 'http://127.0.0.1:8118'
