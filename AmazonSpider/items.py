# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AmazonProductItem(scrapy.Item):
    asin = scrapy.Field()
    title = scrapy.Field()
    categories = scrapy.Field()
    brief_descriptions = scrapy.Field()
    product_description = scrapy.Field()
    product_parameters = scrapy.Field()
    product_details = scrapy.Field()
    brand = scrapy.Field()
    total_review_count = scrapy.Field()
    rating = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
