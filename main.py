#encoding:utf-8
from spider.spider import spider, route, Handler
from os.path import join, dirname, abspath
import _env
from mako.lookup import Template
from BeautifulSoup import BeautifulSoup
import pymongo
import re

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
            print link
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
        if description:
            description = description.text
        smooth_index = soup.findAll(attrs={'class':'pt20'})[0].text
        information = soup.findAll(attrs={'class':'pt20'})[1].text
        tips = soup.find(attrs={'class':'f_s14 pt20'})
        if tips:
            tips = tips.text + tips.nextSibling.nextSibling.text


#        pic1 = soup('a', href="#pic1")[0].find('img')['src']
#        pic2 = soup('a', href="#pic2")[0].find('img')['src']
#        pic3 = soup('a', href="#pic3")[0].find('img')['src']
#        spider.put(HTTP%pic1)
#        spider.put(HTTP%pic2)
#        spider.put(HTTP%pic3)
#        pic4 = soup('a', href="#pic4")
#        if pic4:
#            pic4 = pic4[0].find('img')['src']
#            spider.put(HTTP%pic4)
#        else:
#            pic4 = ''

        #<a href="#pic1">
        # <img title="杜蕾斯大胆爱装避孕套（正面）" src="/images/2012/05/durex_love1.png" alt="杜蕾斯大胆爱装避孕套（正面）" width="73" height="64">
        # </a>
        pics = soup.findAll('a', href = re.compile(r'#pic\d'))
        if pics:
            imageList = []
            for pic in pics:
                img = pic.find('img')['src']
                print img
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
        connection = pymongo.Connection('localhost', 27017)
        db = connection.condom
        collection = db.item

        for link, title, subtitle, description, smooth_index, information, tips, imageList in cls.page:
            item = {"title":title,
                    "subtitle":subtitle,
                    "description":description,
                    "smooth_index":smooth_index,
                    "information":information,
                    "tips":tips,
                    "imageList":imageList
            }
            collection.insert(item)


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
    print fname, 'saved'

if __name__ == '__main__':
    spider.put('http://www.durex.com.cn/products')
    spider.run(5,100)
    item.writedb()

