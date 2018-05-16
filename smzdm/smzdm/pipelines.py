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
        price = item['price'].strip()
        good_name = item['good'].strip()
        good_url = item['url'].strip()
        store = item['store'].strip()
        keyword = item['keyword'].strip()
        
        # 排查已经记录过的信息,如果存在当天的同一条,那么直接删除老数据
        n_date = time.strftime("%Y-%m-%d", time.localtime())
        q_sql = "select id from smzdm where smzdm_url='%s' and discount_date='%s';" % (item['url'], n_date)
        self.cursor.execute(q_sql)
        q_info = self.cursor.fetchone()
        if q_info:
            del_sql = "delete from smzdm where id = '%s';" % (q_info[0], )
            self.cursor.execute(del_sql)
            self.conn.commit()
        else:
            # 新增一条数据就删掉一个关键字所在的最老的数据
            tatal_obj = self.cursor.execute("select count(*) from smzdm where keyword='%s'" % keyword)
            num = tatal_obj.fetchone()[0]
            if num > 40:
                del_sql_key = "delete from smzdm where id in (select id from " \
                              "smzdm where keyword='%s' order by id limit 1 )" % keyword

                self.cursor.execute(del_sql_key)
                self.conn.commit()
        # 加入新数据
        self.cursor.execute("insert into smzdm (name, price, store, smzdm_url, discount_date, keyword) "
                            "values (?, ?, ?, ?, ?, ?)", (good_name,
                                                          price,
                                                          store,
                                                          good_url,
                                                          n_date,
                                                          keyword
                                                          ))
        self.conn.commit()

        # # 每次只保留每个用户,每个关键字的40条记录
        # self.cursor.execute("select distinct key from keywords;")
        # keys_dicts = self.cursor.fetchall()
        # keys = [_key[0] for _key in keys_dicts]
        # for key in keys:
        #     maintain_key = "delete from smzdm where id in (select id from smzdm " \
        #                    "order by id desc limit (select count(*) from smzdm where keyword='%s') offset 10) " % key
        #     print(maintain_key)
        #     self.cursor.execute(maintain_key)
        #     self.conn.commit()
