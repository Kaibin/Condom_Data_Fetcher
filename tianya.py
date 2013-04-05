#encoding:utf-8
from spider.spider import spider, route, Handler
from os.path import join, dirname, abspath
import _env
from mako.lookup import Template
from BeautifulSoup import BeautifulSoup
import pymongo
import re
import requests

PREFIX = join(dirname(abspath(__file__)))
HTTP = 'http://www.tianya.cn%s'

@route('/search/bbs')
class search_page(Handler):
    def get(self):
        content = self.request.content
        soup = BeautifulSoup(''.join(content))
        title = soup.html.head.title
        print title.text
        results = soup.find(attrs={'class':'searchListOne'}).findAll('li')
        for li in results:
            if li.div != None:
                print li.div.h3.a.text
                link = li.div.h3.a['href']
                print link
                spider.put(link)


@route('/post-\w+-\w+-\w\.shtml')
class article(Handler):
    def get(self):
        content = self.request.content
        soup = BeautifulSoup(''.join(content))
        content = soup.find(attrs = {'class':'bbs-content clearfix'}).text
        print content


if __name__ == '__main__':
    spider.put('http://www.tianya.cn/search/bbs?q=安全套&pn=1')
    spider.run(5,100)

