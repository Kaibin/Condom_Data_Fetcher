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
connection = pymongo.Connection('localhost', 27017)
articles = connection['condom']['article']

@route('/article_cat-\d-\d.html')
class article_list(Handler):
    def get(self):
        content = self.request.content
        soup = BeautifulSoup(''.join(content))
        title = soup.html.head.title
        print title.text
        results = soup.find(attrs={'class':'boxCenterList'}).findAll('tr')
        for tr in results:
                if tr.td != None:
                    td = tr.find('td').find('a')
                    article = td['href']
                    print article
                    spider.put(article)

@route('/article-\d+.html')
class article(Handler):
    def get(self):
        content = self.request.content
        soup = BeautifulSoup(''.join(content))
        data = soup.find('div',attrs={'class':'AreaR'}).find('div').find('div')
        title = data.find('font',attrs={'class':'f5 f6'}).text
        print title
        subtitle = data.find('font',attrs={'class':'f3'})
        author = subtitle.text.split('/')[0]
        print author
        date = subtitle.text.split('/')[1]
        print date
        content = ''
        children = data.find('div').findChildren()
        nodes = children[4:-4]
        print nodes
        for child in nodes:
            child = child.text.replace('&nbsp;','')
            child = child.replace('&ldquo;','“')
            child = child.replace('&rdquo;','”')
            child = child.replace('&hellip;','.')
            child = child.replace('&quot;','”')
            content = content + child + "\n"

        article = {'cat_id':4, 'title':title, 'author':author, 'date':date, 'content':content}
        articles.insert(article)


if __name__ == '__main__':
    #cat_id = 1 cat_name = '性用品使用交流'
#    spider.put('http://aiailove.cn/article_cat-4-1.html')
#    spider.put('http://aiailove.cn/article_cat-4-2.html')
#    spider.put('http://aiailove.cn/article_cat-4-3.html')
#    spider.put('http://aiailove.cn/article_cat-4-4.html')
#    spider.put('http://aiailove.cn/article_cat-4-5.html')

    #cat_id = 2 cat_name = '情趣用品使用方法'
#    spider.put('http://aiailove.cn/article_cat-5-1.html')
#    spider.put('http://aiailove.cn/article_cat-5-2.html')
#    spider.put('http://aiailove.cn/article_cat-5-3.html')

    #cat_id = 3 cat_name = '性保健知识'
#    spider.put('http://aiailove.cn/article_cat-6-1.html')
#    spider.put('http://aiailove.cn/article_cat-6-2.html')
#    spider.put('http://aiailove.cn/article_cat-6-3.html')

    #cat_id = 4 cat_name = '成人用品'
    spider.put('http://aiailove.cn/article_cat-7-1.html')
    spider.put('http://aiailove.cn/article_cat-7-2.html')
    spider.put('http://aiailove.cn/article_cat-7-3.html')
    spider.put('http://aiailove.cn/article_cat-7-4.html')

    spider.run(10,100)