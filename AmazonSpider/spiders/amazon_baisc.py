# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import re
from AmazonSpider.items import AmazonProductItem
from AmazonSpider.utils.common import get_md5


class AmazonBaiscSpider(scrapy.Spider):
    name = 'amazon_baisc'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/b?node=289816&ref=Ckwr_sets']
    product_nums = 0

    headers = {
        "HOST": "www.amazon.com",
        "Referer": "https://www.amazon.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def parse(self, response):
        """
        提取出amazon首页中的所有url 并跟踪这些url进行一步爬取
        如果提取的url中格式为 /dp/{ASIN} 或者 /gp/product/{ASIN} 就下载之后直接进入解析函数
        ASIN号为amazon产品的唯一代码，由10位数字和字母组成
        """
        if AmazonBaiscSpider.product_nums < 10:
            all_urls = response.css("a::attr(href)").extract()
            all_urls = [parse.urljoin(response.url, url) for url in all_urls]
            # all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
            for url in all_urls:
                match_obj = re.match(r"https://www.amazon.com/.*(dp/|gp/product/)([A-Za-z0-9]{10})(/|$).*", url)
                if match_obj:
                    # amazon产品页面
                    asin = match_obj.group(2)
                    AmazonBaiscSpider.product_nums += 1
                    yield scrapy.Request(url, headers=self.headers, callback=self.parse_product,
                                         meta={"asin": asin})
                else:
                    # 非amazon产品页面，直接进一步跟踪
                    yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_product(self, response):
        asin = response.meta.get("asin", "")
        title = response.css("#title #productTitle::text").extract_first("").strip()
        categories = response.css("#wayfinding-breadcrumbs_feature_div .a-unordered-list .a-list-item a::text").extract()
        categories = [category.strip() for category in categories]
        brief_descriptions = response.css("#feature-bullets .a-unordered-list .a-list-item::text").extract()
        brief_descriptions = [brief_description.strip() for brief_description in brief_descriptions if brief_description.strip()]
        product_description = response.css("#productDescription p::text").extract_first("").strip()
        product_parameters_node = response.css("#productDetails_detailBullets_sections1 tr")
        product_parameters = {tr_node.css("th::text").extract_first("").strip(): "".join([value.strip() for value in tr_node.css("td::text").extract()]) for tr_node in product_parameters_node}

        product_details = response.css("#aplus_feature_div").extract_first("").replace("\n", "")
        brand = response.css("#bylineInfo::text").extract_first("")
        total_review_count = response.css(".totalReviewCount::text").extract_first("")
        rating = response.css(".arp-rating-out-of-text::text").extract_first("")
        url = response.url

        product_item = AmazonProductItem()
        product_item['asin'] = asin
        product_item['title'] = title
        product_item['categories'] = categories
        product_item['brief_descriptions'] = brief_descriptions
        product_item['product_description'] = product_description
        product_item['product_parameters'] = product_parameters
        product_item['product_details'] = product_details
        product_item['brand'] = brand
        product_item['total_review_count'] = total_review_count
        product_item['rating'] = rating
        product_item['url'] = url
        product_item['url_object_id'] = get_md5(url)

        print(product_item)

