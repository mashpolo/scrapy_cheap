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
    start_urls = ["http://search.smzdm.com/?c=faxian&s=拖鞋&v=a"]

    def parse(self, response):
        # We want to inspect one specific response.
        items = response.xpath("//div/ul[contains(@id, 'feed-main-list')]/li[contains(@class, 'feed-row-wide')]")
        whole_info = []
        for item in items:
            info = item.xpath("//h5[@class='feed-block-title']/a/text()")[0].extract()
            whole_info.append(info.strip())

        print whole_info[3]