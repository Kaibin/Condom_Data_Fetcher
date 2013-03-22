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
#    url = 'http://www.yeedou.com/anquantao-c2441/product-picture-51976419.html'
#    content = requests.get(url,timeout=300).content
#    soup = BeautifulSoup(''.join(content))
#    results = soup.find(attrs={"class":"gundong"})
#    results = results.findAll('li')[1:-1]
#    for result in results:
#        pic = result.find('a')
#        img = pic['href']
#        url = 'http://www.yeedou.com%s'
#        print url%img
#        content = requests.get(url%img).content
#        soup = BeautifulSoup(''.join(content))
#        div = soup.find(attrs={"class":"mainbg"}).find(attrs={"type":"text/javascript"})
#        print div.text
#        start = div.text.find("http")
#        end = div.text.find('");')
#        print div.text[start:end]


#    tips = """倍力乐夜光安全套 7P描述提示：以下信息来源于爱之谷：【功 效】本品能够安全有效避孕。在正确使用方式下，可降低感染艾滋病和其他性病的机会，例如病原体、生殖道疱疹、淋病、梅毒等。使用时无任何异物感，能最充分的激发快感。【标称阔度】52&plusmn;2mm【标称长度】180&plusmn;5mm【标称厚度】0.069mm【包装规格】<!--[if gte mso 9]><xml> <w:WordDocument> <w:View>Normal</w:View> <w:Zoom>0</w:Zoom> <w:PunctuationKerning  /> <w:DrawingGridVerticalSpacing>7.8 磅</w:DrawingGridVerticalSpacing> <w:DisplayHorizontalDrawingGridEvery>0</w:DisplayHorizontalDrawingGridEvery> <w:DisplayVerticalDrawingGridEvery>2</w:DisplayVerticalDrawingGridEvery> <w:ValidateAgainstSchemas  /> <w:SaveIfXMLInvalid>false</w:SaveIfXMLInvalid> <w:IgnoreMixedContent>false</w:IgnoreMixedContent> <w:AlwaysShowPlaceholderText>false</w:AlwaysShowPlaceholderText> <w:Compatibility> <w:SpaceForUL  /> <w:BalanceSingleByteDoubleByteWidth  /> <w:DoNotLeaveBackslashAlone  /> <w:ULTrailSpace  /> <w:DoNotExpandShiftReturn  /> <w:AdjustLineHeightInTable  /> <w:BreakWrappedTables  /> <w:SnapToGridInCell  /> <w:WrapTextWithPunct  /> <w:UseAsianBreakRules  /> <w:DontGrowAutofit  /> <w:UseFELayout  /> </w:Compatibility> <w:BrowserLevel>MicrosoftInternetExplorer4</w:BrowserLevel> </w:WordDocument> </xml><![endif][if gte mso 9]><xml> <w:LatentStyles DefLockedState="false" LatentStyleCount="156"> </w:LatentStyles> </xml><![endif][if gte mso 10]> <style> /* Style Definitions */ table.MsoNormalTable {mso-style-name:普通表格; mso-tstyle-rowband-size:0; mso-tstyle-colband-size:0; mso-style-noshow:yes; mso-style-parent:""; mso-padding-alt:0cm 5.4pt 0cm 5.4pt; mso-para-margin:0cm; mso-para-margin-bottom:.0001pt; mso-pagination:widow-orphan; font-size:10.0pt; font-family:"Times New Roman"; mso-fareast-font-family:"Times New Roman"; mso-ansi-language:#0400; mso-fareast-language:#0400; mso-bidi-language:#0400;} </style> <![endif]7支装 （每盒含有3只夜光型安全套+4只超薄型安全套）【成 份】马来西亚指定橡胶园供应，特级天然乳胶！【认证信息】ISO4074；CE600；GB7544-99；ccc等等【执行标准】执行标准：ISO4074；CE600；GB7544-99【生产许可证】进口医疗器械注册：国食药监械（进）字2004第2461869号，强制性产品认证证书：2004071501000337。 -->"""
#    tips = re.sub(r'<.+>', '', tips)
#    print tips

    link = 'www.baidu.com'
    print 'I hate ' + link