import scrapy
from blbl.items import BlblItem
import requests
from bs4 import BeautifulSoup
import json

class BlblSpiderSpider(scrapy.Spider):
    name = 'blbl_spider'
    allowed_domains = ['bilibili.com']
    keyword = input("请输入查询关键字")
    start_urls = ['https://search.bilibili.com/video?keyword={}'.format(keyword)]
    def parse(self,response):
        keyword = self.keyword
        #获取标题和作者
        videolist = response.xpath("//ul[@class='video-list clearfix']/li")
        titles = []
        authors = []
        for video in videolist:
            title = video.xpath(".//a[@class='title']/@title").get()
            author = video.xpath(".//a[@class='up-name']/text()").get()
            titles.append(title)
            authors.append(author)
        #获取script内容
        script = response.xpath('//script/text()')[2].get().replace('window.__INITIAL_STATE__=','').replace(';(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());','')
        #转换为字典方便后续筛选
        script = json.loads(script)
        #筛选图片地址
        result = script['flow']
        result1 = result['getSingleTypeList-jump-keyword-{}-search_type-video'.format(keyword)]
        result2 = result1['result']

        for i in range(len(result2)):
            imgurl = ['https:'+result2[i]['pic']]
            title = titles[i]
            author = authors[i]
            data = BlblItem(title=title,author=author,image_urls=imgurl)
            yield data

    