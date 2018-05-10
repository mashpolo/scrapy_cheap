# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import time


class SmzdmPipeline(object):
    def __init__(self):
        self.conn = sqlite3.connect("./smzdm.db")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        self.cursor.execute("insert into smzdm (good, price, smzdm_url, discount_date) "
                            "values (?, ?, ?, ?)", (item['good'].strip(),
                                                    item['price'].strip(),
                                                    item['url'].strip(),
                                                    time.strftime("%Y-%m-%d",
                                                                  time.localtime())
                                                    ))
        self.conn.commit()
        # self.conn.close()
