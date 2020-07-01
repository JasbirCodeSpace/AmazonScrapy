# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class ProductPipeline:
	db_file = 'amazon-product.db'
	db_table = 'amazon_product' 
	def __init__(self):
		self.create_connection()
		self.create_table()

	def create_connection(self):
		self.conn = sqlite3.connect(self.db_file)
		self.curr = self.conn.cursor()

	def create_table(self):
		self.curr.execute(""" DROP TABLE IF EXISTS %s """ % self.db_table)
		self.curr.execute(""" CREATE TABLE %s (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT,
			brand TEXT,
			price TEXT,
			availability TEXT,
			shipping TEXT,
			features TEXT,
			ratings TEXT,
			image TEXT)""" % self.db_table)
		self.conn.commit()


	def insert_row(self,item):
		self.curr.execute(""" INSERT INTO %s (name,brand,price,availability,shipping,features,ratings,image) 
			VALUES(?,?,?,?,?,?,?,?)""" % self.db_table,(
			item['product_name'],
			item['product_brand'],
			item['product_price'],
			item['product_availability'],
			item['product_shipping'],
			item['product_features'],
			item['product_ratings'],
			item['product_image']))
		self.conn.commit()

	def process_item(self, item, spider):
		self.insert_row(item)
		return item
