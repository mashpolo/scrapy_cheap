#!/usr/bin/env python
# encoding: utf-8
"""
desc:   爬取 url 列表
author: lu.luo
date:  2018-04-02
"""
import scrapy


class MySpider(scrapy.Spider):
    name = "smzdm"
    start_urls = ["http://search.smzdm.com/?c=faxian&s=Nintendo Switch&v=a"]

    def parse(self, response):
        # We want to inspect one specific response.
        items = response.xpath("//div/ul[@id='feed-main-list']/li")
        for item in items:
            info = item.xpath(".//h5[@class='feed-block-title']/a/text()").extract_first()
            prince = item.xpath(".//a/div[@class='z-highlight']/text()").extract_first()
            print(info, prince)

