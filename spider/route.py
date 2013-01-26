#coding:utf-8

import re

# 类装饰器
class Route(object):
    def __init__(self):
        self.map = []

    #   通过__call__属性，类成为可调用对象
    def __call__(self, path):
        if not path.endswith('$'):
            path += '$'
        re_path = re.compile(path)
        def _(func):    #func表示被装饰的函数
            self.map.append((re_path, func))
            return func
        return _

    def match(self, url):
        for reg, func in self.map:
            m = reg.match(url)
            if m:
                self.path = url
                return func, m.groups()
        print 'WARNING: ', url, 'not match any handler'
        return None, None
