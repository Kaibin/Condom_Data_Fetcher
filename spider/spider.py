#coding:utf-8
from gevent import monkey
monkey.patch_all()
from gevent.queue import Empty,Queue
import gevent
import requests
from urlparse import urlparse, parse_qs
from route import Route
from gevent.pool import Pool

class Spider(object):
    cookie = None
    headers = {}

    def __init__(self, route):
        self.queue = Queue()
        self.route = route

    def _fetch(self):
        queue = self.queue
        timeout = self.timeout
        route = self.route
        while True:
            try:
                url = queue.get(timeout = timeout + 100)
            except Empty:
                return

            headers = self.headers

            if self.cookie:
                headers['Cookie'] = self.cookie

            req = requests.get(url, timeout = timeout, headers = headers)
            p = urlparse(req.url)
            cls, args = route.match(p.path)
            if cls:
                o = cls(req)  #构造一个Handler对象
                r = o.get(*args)
                if r:
                    for i in r:
                        if i:
                            queue.put(i)

    def run(self, num=20, timeout=600):
        self.timeout = timeout
        threads = [gevent.spawn(self._fetch) for i in xrange(num)]
        gevent.joinall(threads)

    def put(self, url):
        self.queue.put(url)

class Handler(object):
    def __init__(self, request):
        p = urlparse(request.url)
        request.arguments = parse_qs(p.query, 1)
        self.request = request
        self.html = request.content

    def get_argument(self, name, default=None):
        result = self.request.arguments.get(name, None)
        if result is None:
            return default
        return result[0].encode('utf-8', 'ignore')

route = Route()
spider = Spider(route)