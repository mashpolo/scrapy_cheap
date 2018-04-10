#!/usr/bin/env python
# encoding: utf-8
"""
desc:
author: lu.luo
date:  2018-04-02
"""
import scrapy


class MySpider(scrapy.Spider):
    name = "smzdm"
    start_urls = ["http://search.smzdm.com/?c=faxian&s=%E6%89%8B%E6%9C%BA&v=a"]

    def parse(self, response):
        # We want to inspect one specific response.
        #items = response.xpath("//div/ul[@id='feed-main-list']/li[@class='feed-row-wide']")
        items = response.xpath('//ul[@id="feed-main-list"]/li')
        print len(items)
        sss = items[19].xpath('//h5[@class="feed-block-title"]')
        infos = sss[19].xpath("//a[@class='feed-nowrap']/@title").extract()
        prices = sss[19].xpath("//a/div/text()").extract()
        for (i, x) in enumerate(infos):
            print x
            print prices[i+1]
        # for item in items:
        #     info = item.xpath("//h5[@class='feed-block-title']/a/text()")[0]
        #     print info

