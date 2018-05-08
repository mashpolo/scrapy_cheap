# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class SmzdmPipeline(object):

    def __init__(self):
        self.file = open('items', 'wb')

    def process_item(self, item, spider):
        line = item['good'].strip() + ":" + item['price'] + '\n'
        print(line)
        # self.file.write(line)
