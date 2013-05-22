#encoding:utf-8
from spider.spider import spider, route, Handler
from os.path import join, dirname, abspath
import _env
from BeautifulSoup import BeautifulSoup
import pymongo

PREFIX = join(dirname(abspath(__file__)))
HTTP = 'http://aiailove.cn/%s'

@route('/category-29-b0.html')
class goodlist(Handler):
    def get(self):
        content = self.request.content
        soup = BeautifulSoup(''.join(content))
        result = soup.find(attrs={'class':'centerPadd'}).find(attrs={'class':'clearfix goodsBox'}).findAll('div')
        for div in result:
            link = div.a['href']
            print 'Fetch condom from ' + link
            spider.put(link)

@route('/goods-\d+.html')
class goodItem(Handler):
    def get(self):
        content = self.request.content
        soup = BeautifulSoup(''.join(content))

if __name__ == '__main__':
    spider.put('http://aiailove.cn/category-29-b0.html')
    spider.run(5,100)

