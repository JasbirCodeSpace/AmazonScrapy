# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field()
    product_brand = scrapy.Field()
    product_image = scrapy.Field()
    product_price = scrapy.Field()
    product_availability = scrapy.Field()
    product_shipping = scrapy.Field()
    product_features = scrapy.Field()
    product_average_rating = scrapy.Field()
    
