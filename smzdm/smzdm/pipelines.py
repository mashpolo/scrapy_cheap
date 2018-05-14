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
        # 优化价格的展示形式
        price = item['price'].split('（')[0].strip()
        good_name = item['good'].strip()
        good_url = item['url'].strip()
        store = item['store'].strip()
        
        # 排查已经记录过的信息,如果存在当天的同一条,那么直接删除老数据
        n_date = time.strftime("%Y-%m-%d", time.localtime())
        q_sql = "select id from smzdm where smzdm_url='%s' and discount_date='%s';" % (item['url'], n_date)
        self.cursor.execute(q_sql)
        q_info = self.cursor.fetchone()
        if q_info:
            del_sql = "delete from smzdm where id = '%s';" % (q_info[0], )
            self.cursor.execute(del_sql)
            self.conn.commit()

        self.cursor.execute("insert into smzdm (name, price, store, smzdm_url, discount_date, user_id) "
                            "values (?, ?, ?, ?, ?, ?)", (good_name,
                                                          price,
                                                          store,
                                                          good_url,
                                                          n_date,
                                                          1
                                                          ))
        self.conn.commit()
