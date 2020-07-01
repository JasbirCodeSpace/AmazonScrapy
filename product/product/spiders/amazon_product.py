# -*- coding: utf-8 -*-
import scrapy


class AmazonProductSpider(scrapy.Spider):
    name = 'amazon_product'
    allowed_domains = ['amazon.in']
    start_urls = ['http://amazon.in/']

    def parse(self, response):
        pass
