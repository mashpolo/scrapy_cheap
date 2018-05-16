#!/usr/bin/env python
# encoding: utf-8
"""
desc:   爬取 url 列表
author: lu.luo
date:  2018-04-02
"""
import scrapy
import sqlite3

from ..items import SmzdmItem


class MySpider(scrapy.Spider):
    name = "smzdm"
    url_models = ["http://search.smzdm.com/?c=faxian&s={0}&v=a",
                  "http://search.smzdm.com/?c=faxian&s={0}&v=a&p=2"]
    conn = sqlite3.connect("./smzdm.db")
    cursor = conn.cursor()
    cursor.execute("select distinct key from keywords;")
    keys_dicts = cursor.fetchall()
    keys = [_key[0] for _key in keys_dicts]

    # start urls
    start_urls = []
    for key in keys:
        for url in url_models:
            add_url = url.format(key)
            start_urls.append(add_url)

    def parse(self, response):
        # We want to inspect one specific response.
        items = response.xpath("//div/ul[@id='feed-main-list']/li")
        key = response.xpath("//input[@id='J_search_input']/@value").extract_first()
        for item in items:
            info = SmzdmItem()
            info["good"] = item.xpath(".//h5[@class='feed-block-title']/a/text()").extract_first()
            info["price"] = item.xpath(".//a/div[@class='z-highlight']/text()").extract_first()
            info["url"] = item.xpath(".//div[@class='feed-link-btn-inner']/a/@href").extract_first()
            info["store"] = item.xpath(".//span[@class='feed-block-extras']/span/text()").extract_first()
            info["keyword"] = key
            yield info

