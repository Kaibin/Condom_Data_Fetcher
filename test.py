#coding:utf-8

import requests
from spider.spider import spider, route, Handler
from os.path import join, dirname, abspath
import _env
from mako.lookup import Template
from BeautifulSoup import BeautifulSoup
import pymongo
import re
import urllib2

if __name__ == '__main__':
    url = 'http://www.yeedou.com/anquantao-c2441/product-picture-51976419.html'
    content = requests.get(url,timeout=300).content
    soup = BeautifulSoup(''.join(content))
    results = soup.find(attrs={"class":"gundong"})
    results = results.findAll('li')[1:-1]
    for result in results:
        pic = result.find('a')
        img = pic['href']
        url = 'http://www.yeedou.com%s'
        print url%img
        content = requests.get(url%img).content
        soup = BeautifulSoup(''.join(content))
        div = soup.find(attrs={"class":"mainbg"}).find(attrs={"type":"text/javascript"})
        print div.text
        start = div.text.find("http")
        end = div.text.find('");')
        print div.text[start:end]

