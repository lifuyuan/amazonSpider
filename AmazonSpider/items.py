# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json
from random import randint


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
    images = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into az_products(url, name, brand, score, details, images, product_parameters, categories,
            asin, description, product_sku, comments_count, short_description) values (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (self["url"], self["title"], self["brand"], self["rating"],
                  self["product_details"], self["images"], json.dumps(self["product_parameters"]), self["categories"],
                  self["asin"], self["product_description"], [], randint(1, 200), self["brief_descriptions"])

        return insert_sql, params
