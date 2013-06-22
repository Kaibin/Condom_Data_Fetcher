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
HTTP = 'http://aiailove.cn/%s'

# connect to the database
#connection = pymongo.Connection('localhost', 27017)
#articles = connection['condom']['article']

@route('/article_cat-\d-\d.html')
class article_list(Handler):
    def get(self):
        url = route.path
        p = re.compile('\d')
        m = p.findall(url)[0]
        m = int(m)-3

        content = self.request.content
        soup = BeautifulSoup(''.join(content))
        title = soup.html.head.title
        print title.text
        results = soup.find(attrs={'class':'boxCenterList'}).findAll('tr')
        for tr in results:
                if tr.td != None:
                    td = tr.find('td').find('a')
                    article = td['href']
                    article = article +'?cat_id=' + str(m)
                    spider.put(article)

@route('/article-\d+.html')
class article(Handler):
    def get(self):
        cat_id = self.request.arguments['cat_id'][0]
        content = self.request.content
        soup = BeautifulSoup(''.join(content))
        data = soup.find('div',attrs={'class':'AreaR'}).find('div').find('div')
        title = data.find('font',attrs={'class':'f5 f6'}).text
#        print title
        subtitle = data.find('font',attrs={'class':'f3'})
        author = subtitle.text.split('/')[0]
#        print author
        date = subtitle.text.split('/')[1]
#        print date
        content = ''
        children = data.find('div').findChildren()
        nodes = children[4:-4]
#        print nodes
        for child in nodes:
            child = child.text.replace('&nbsp;','')
            child = child.replace('&ldquo;','“')
            child = child.replace('&rdquo;','”')
            child = child.replace('&hellip;','.')
            child = child.replace('&quot;','”')
            content = content + child + "\n"
        article = {'cat_id':cat_id, 'title':title, 'author':author, 'date':date, 'content':content}
        articles.insert(article)

if __name__ == '__main__':
    #cat_id = 1 cat_name = '性用品使用交流'
    for i in xrange(1,6):
        url = 'http://aiailove.cn/article_cat-4-%s.html' % i
        spider.put(url)

    #cat_id = 2 cat_name = '情趣用品使用方法'
    for i in xrange(1,4):
        url = 'http://aiailove.cn/article_cat-5-%s.html' % i
        spider.put(url)

    #cat_id = 3 cat_name = '性保健知识'
    for i in xrange(1,4):
        url = 'http://aiailove.cn/article_cat-6-%s.html' % i
        spider.put(url)

    #cat_id = 4 cat_name = '成人用品'
    for i in xrange(1,5):
        url = 'http://aiailove.cn/article_cat-7-%s.html' % i
        spider.put(url)

    spider.run(10,100)