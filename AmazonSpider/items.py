# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json


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

    def get_insert_sql(self):
        insert_sql = """
            insert into amazon_products(asin, title, categories, brief_descriptions, product_description,
            product_parameters, product_details, brand, total_review_count, rating, url, url_object_id) values (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (self["asin"], self["title"], self["categories"], self["brief_descriptions"],
                  self["product_description"], json.dumps(self["product_parameters"]), self["product_details"],
                  self["brand"], self["total_review_count"].replace(",", ""), self["rating"], self["url"], self["url_object_id"])

        return insert_sql, params
