#encoding:utf-8
from spider.spider import spider, route, Handler
from os.path import join, dirname, abspath
import _env
from mako.lookup import Template
from BeautifulSoup import BeautifulSoup
import pymongo
import re
import solr

PREFIX = join(dirname(abspath(__file__)))
HTTP = 'http://www.durex.com.cn%s'

@route('/products/')
class products(Handler):
    def get(self):
        content = self.request.content
        soup = BeautifulSoup(''.join(content))
        result = soup.find(attrs={'class':'products'}).findAll('li')
        for li in result:
            link = li.p.a['href']
            print 'Fetch condom from ' + link
            spider.put(HTTP%link)

@route('/products/\w+-?\w*-?\w*-?\w*/')
class item(Handler):
    template = Template(filename=join(PREFIX,'template/json.template'))
    page = []

    def get(self):
        content = self.request.content
        soup = BeautifulSoup(''.join(content))

        #所有text已经被自动转为unicode，如果需要，可以自行转码encode(xxx)
        title = soup.html.body.h1
        if not title:
            return
        title = title.text
        subtitle = soup.findAll(attrs={'class':'f_cy f_s16b'})[0].string
        description = soup.find(attrs={'class':'f_cy f_s14 pt20'})
        description = description.text if description else ''
        smooth_index = soup.findAll(attrs={'class':'pt20'})[0]
        smooth_index = smooth_index.text if smooth_index else ''
        information = soup.findAll(attrs={'class':'pt20'})[1]
        information = information.text if information else ''
        tips = soup.find(attrs={'class':'f_s14 pt20'})
        tips = tips.text + tips.nextSibling.nextSibling.text if tips else ''

#        pics = soup.findAll('a', href = re.compile(r'pic\d'))
        pics = soup.findAll(attrs={'class':'pic1'})
        if pics:
            imageList = []
            for pic in pics:
                img = pic.find('img')['src']
                imageList.append(img)
                spider.put(HTTP%img)

        self.page.append((self.request.url, title, subtitle, description, smooth_index, information, tips, imageList))

    @classmethod
    def write(cls):
        page = cls.page
        with open(join(PREFIX, 'durex.txt'), 'w') as rss:
            rss.write(
                cls.template.render(
                    data = [
                        dict(
                            title = title,
                            subtitle = subtitle,
                            description = description,
                            smooth_index = smooth_index,
                            information = information,
                            tips = tips,
                            imageList = imageList
                        ) for link, title, subtitle, description, smooth_index, information, tips, imageList in cls.page
                    ]
                )
            )

    @classmethod
    def writedb(cls):
        page = cls.page
        # create connection to mongodb
        connection = pymongo.Connection('localhost', 27017)
        db = connection.condom
        collection = db.item
        # create connection to solr server
        solrConnection = solr.SolrConnection('http://127.0.0.1:8983/solr')

        for link, title, subtitle, description, smooth_index, information, tips, imageList in cls.page:
            item = {
                    "title":title,
                    "subtitle":subtitle,
                    "description":description,
                    "smooth_index":smooth_index,
                    "information":information,
                    "tips":tips,
                    "imageList":imageList
            }
#           insert item into mongodb
            doc_id = collection.insert(item)
#           add a document to the index
            solrConnection.add(id = doc_id, title = item.get('title'), description = item.get('description'), subtitle = item.get('subtitle'), information = item.get('information'))
#           commit to solr
        solrConnection.commit()

@route('/images/.+')
class pic(Handler):
    def get(self):
        save_pic(self.html, route.path.split('/')[-1])

@route('/wp-content/uploads/.+')
class pic2(Handler):
    def get(self):
        save_pic(self.html, route.path.split('/')[-1])


def save_pic(content, fname):
    basepath = join(PREFIX, 'images')
    fpath = join(basepath, fname)
    f = open(fpath, 'wb')
    f.write(content)
    f.close()
    print 'Download image: ' + fname

if __name__ == '__main__':
    spider.put('http://www.durex.com.cn/products')
    spider.run(5,100)
    item.writedb()

