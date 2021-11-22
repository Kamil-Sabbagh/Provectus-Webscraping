from stem import Signal
from stem.control import Controller
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from stem.util.log import get_logger

from .settings import REQUESTS_PER_SAME_TOR_IDENTITY


# Number of requests sent during the current tor identity
NUM_SENT_REQUESTS = 0


def new_tor_identity():
    with Controller.from_port(port=9051) as controller:
        # authenticate with the tor password
        controller.authenticate(password='027D1370DD5D27AA602286D179466905FD6A15778772556AFBAE310CCD')

        # Change tor identity
        controller.signal(Signal.NEWNYM)


class ProxyMiddleware(HttpProxyMiddleware):

    def process_response(self, request, response, spider):

        # Get a new identity depending on the response
        if response.status != 200:
            new_tor_identity()
            NUM_SENT_REQUESTS
            return request

        return response

    def process_request(self, request, spider):
        global NUM_SENT_REQUESTS
        # Set the Proxy
        # A new identity for each N requests request

        if NUM_SENT_REQUESTS >= REQUESTS_PER_SAME_TOR_IDENTITY:
            NUM_SENT_REQUESTS = 0
            new_tor_identity()

        NUM_SENT_REQUESTS += 1

        # add a proxy for the response
        request.meta['proxy'] = 'http://127.0.0.1:8118'
