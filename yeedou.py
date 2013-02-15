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

        brand = soup.find('span',attrs={'class':'b'}).nextSibling.text
        brand = brand.replace('安全套','')
        if '（' in brand:
            index = brand.index('（')
            brand = brand[0:index]

        description = soup.find(attrs={'class':'desc'})
        description = description.text if description else ''

        canshu = soup.findAll(attrs={'class':'canshu'})
        if canshu[0]:
            information = canshu[0].text
            tips = ''
        if len(canshu) > 1:
            tips = canshu[1].text

        pics = soup.findAll('a',href=re.compile(r'/anquantao-c2441/product-picture-\d+.html'))
        if pics:
            imageList = []
            for pic in pics:
                img = pic['href']
                print img
                content = requests.get(HTTP%img,timeout=1000).content
                soup = BeautifulSoup(''.join(content))
                div = soup.find(attrs={"class":"mainbg"}).find(attrs={"type":"text/javascript"})
                start = div.text.find("http")
                end = div.text.find('");')
                imgSrc = div.text[start:end]
                print imgSrc
                imageList.append(imgSrc)
                save_pic(requests.get(imgSrc,timeout=1000).content, imgSrc.split('/')[-1])

        self.page.append((self.request.url, title, brand, description, information, tips, imageList))

    @classmethod
    def writedb(cls):
        page = cls.page
        connection = pymongo.Connection('localhost', 27017)
        db = connection.condom
        collection = db.item2

        for link, title, brand, description, information, tips, imageList in cls.page:
            item = {"title":title,
                    "brand":brand,
                    "description":description,
                    "information":information,
                    "tips":tips,
                    "imageList":imageList
            }
            collection.insert(item)

#
#@route('/images/.+')
#class pic(Handler):
#    def get(self):
#        save_pic(self.html, route.path.split('/')[-1])

#@route('/anquantao-c2441/product-picture-\d+.html')
#class picture(Handler):
#    def get(self):
#        content = self.request.content
#        soup = BeautifulSoup(''.join(content))
#        img = soup.find('img',attrs={"id":"BIGIMG"})
#        imgSrc = img['src']

def save_pic(content, fname):
    basepath = join(PREFIX, 'images2')
    fpath = join(basepath, fname)
    f = open(fpath, 'wb')
    f.write(content)
    f.close()
    print fname, 'saved'


if __name__ == '__main__':
    spider.put('http://www.yeedou.com/anquantao-c2441/')
    spider.run(5,1000)
    item.writedb()