#encoding:utf-8
from spider.spider import spider, route, Handler
from os.path import join, dirname, abspath
import _env
from mako.lookup import Template
from BeautifulSoup import BeautifulSoup
import pymongo
import re
import requests
import solr

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
            number = filter(lambda ch: ch in '0123456789', li.text)
            print 'Condom number:' + number
            page_size = 20
            page_num = 0
            if(int(number)%page_size != 0):
                page_num = int(number)/page_size + 1
            else:
                page_num = int(number)/page_size
            for pn in range(page_num):
                page = pn+1
                url = link +'pn' +str(page)
                print 'Fetch condom from ' + HTTP%url
                spider.put(HTTP%url)

@route('/\w+-\w+/anquantao-c2441/\w*')
class itemlist(Handler):
    def get(self):
        content = self.request.content
        soup = BeautifulSoup(''.join(content))
        result = soup.findAll(attrs={"class":"title"})
        print self.request.url + ': ' + str(result)
        for li in result:
            link = li['href']
            link = link.replace('price','detail')
#            print link
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
        if '【' in description:
            index = description.index('【')
            description = description[0:index]
        description = description.replace('&#177;','±')

        spans = soup.findAll('span',attrs={'class':'b'})
        if spans[3]:
            span = spans[3]
            price = span.nextSibling.text
            price = price.replace('&yen;','¥')

        canshu = soup.findAll(attrs={'class':'canshu'})
        if canshu[0]:
            information = canshu[0].text
            tips = ''
        if len(canshu) > 1:
            tips = canshu[1].text
            tips = re.sub(r'[.+]', '', tips)
            tips = re.sub(r'<.+>', '', tips)
            tips = tips.replace('●','\n●')
            tips = tips.replace('【','\n【')
            tips = tips.replace('&plusmn;','±')
            tips = tips.replace('&nbsp;','')
            tips = tips.replace('&ldquo;','“')
            tips = tips.replace('&rdquo;','”')
            tips = tips.replace('&mdash;','-')
            tips = tips.replace('&quot;','”')
            tips = tips.replace('描述','')
            tips = tips.replace('基本信息','\n基本信息：')
            tips = tips.replace('温馨提示','\n温馨提示：')
            tips = tips.replace('品牌介绍','\n品牌介绍：\n')

        pics = soup.findAll('a',href=re.compile(r'/anquantao-c2441/product-picture-\d+.html'))
        if pics:
            imageList = []
            for pic in pics:
                img = pic['href']
#                print img
                content = requests.get(HTTP%img,timeout=1000).content
                soup = BeautifulSoup(''.join(content))
                div = soup.find(attrs={"class":"mainbg"}).find(attrs={"type":"text/javascript"})
                start = div.text.find("http")
                end = div.text.find('");')
                imgSrc = div.text[start:end]
                imageList.append(imgSrc)
                save_pic(requests.get(imgSrc,timeout=1000).content, imgSrc.split('/')[-1])

        self.page.append((self.request.url, title, brand, description, price, information, tips, imageList))

    @classmethod
    def writedb(cls):
        page = cls.page
        # create connection to mongodb
        connection = pymongo.Connection('localhost', 27017)
        db = connection.condom
        collection = db.item2
        # create connection to solr server
        solrConnection = solr.SolrConnection('http://127.0.0.1:8983/solr')

        for link, title, brand, description, price, information, tips, imageList in cls.page:
            item = {
                    "title":title,
                    "brand":brand,
                    "description":description,
                    "price":price,
                    "information":information,
                    "tips":tips,
                    "imageList":imageList
            }
#            insert item into mongodb
            doc_id = collection.insert(item)
#            add a document to the index
            solrConnection.add(id = doc_id, title = item.get('title'), description = item.get('description'), brand = item.get('brand'), information = item.get('information'))
#        commit to solr
        solrConnection.commit()

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
    basepath = join(PREFIX, 'images_yeedou')
    fpath = join(basepath, fname)
    f = open(fpath, 'wb')
    f.write(content)
    f.close()
    print 'Download image: ' + fname

if __name__ == '__main__':
    spider.put('http://www.yeedou.com/anquantao-c2441/')
    spider.run(5,1000)
    item.writedb()