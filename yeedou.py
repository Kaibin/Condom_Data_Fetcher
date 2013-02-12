#encoding:utf-8
from spider.spider import spider, route, Handler
from os.path import join, dirname, abspath
import _env
from mako.lookup import Template
from BeautifulSoup import BeautifulSoup
import pymongo
import re

PREFIX = join(dirname(abspath(__file__)))
HTTP = 'http://www.yeedou.com%s'

@route('/anquantao-c2441/')
class anquantao(Handler):
    def get(self):
        content = self.request.content
        soup = BeautifulSoup(''.join(content))
        result = soup.find(attrs={"class":"leftinnersubmenu sidebar"}).findAll('li')
        for li in result:
            link = li.a['href']
            print link
            spider.put(HTTP%link)

@route('/\w+-\w+/anquantao-c2441/')
class itemlist(Handler):
    def get(self):
        content = self.request.content
        soup = BeautifulSoup(''.join(content))
        result = soup.findAll(attrs={"class":"title"})
        for li in result:
            link = li['href']
            link = link.replace('price','detail')
            print link
            spider.put(HTTP%link)

@route('/anquantao-c2441/product-detail-\d+.html')
class item(Handler):
    page = []
    def get(self):
        content = self.request.content
        soup = BeautifulSoup(''.join(content))

        title = soup.html.body.h1
        if not title:
            return
        title = title.text
        description = soup.find(attrs={'class':'desc'})
        description = description.text if description else ''
        canshu = soup.findAll(attrs={'class':'canshu'})
        if canshu[0]:
            information = canshu[0].text
            tips = ''
#            print information
        if len(canshu) > 1:
            tips = canshu[1].text
#            print tips.text

        pics = soup.findAll('a',href=re.compile(r'/anquantao-c2441/product-picture-\d+.html'))
        if pics:
            imageList = []
            for pic in pics:
                img = pic.find('img')['src']
                imageList.append(img)
                print img
                spider.put(img)

        self.page.append((self.request.url, title, description, information, tips, imageList))

    @classmethod
    def writedb(cls):
        page = cls.page
        connection = pymongo.Connection('localhost', 27017)
        db = connection.condom
        collection = db.item2

        for link, title, description, information, tips, imageList in cls.page:
            item = {"title":title,
                    "description":description,
                    "information":information,
                    "tips":tips,
                    "imageList":imageList
            }
            collection.insert(item)


@route('/images/.+')
class pic(Handler):
    def get(self):
        save_pic(self.html, route.path.split('/')[-1])


def save_pic(content, fname):
    basepath = join(PREFIX, 'images2')
    fpath = join(basepath, fname)
    f = open(fpath, 'wb')
    f.write(content)
    f.close()
    print fname, 'saved'


if __name__ == '__main__':
    spider.put('http://www.yeedou.com/anquantao-c2441/')
    spider.run(5,300)
    item.writedb()
