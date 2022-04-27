import scrapy
import json
from ..items import War2022Team777Item
import hashlib


class GazetaArticlesSpider(scrapy.Spider):
    name = 'gazeta_articles'
    allowed_domains = ['m.gazeta.ru']
    start_urls = []

    def start_requests(self):
        # Open the JSON file which contains article links
        data = []
        with open('./gazeta.json') as json_file:
            data = json.load(json_file)

        for link_url in data:
            print('URL: ' + link_url['article_url'])
            # Request to get the HTML content
            request = scrapy.http.Request(link_url['article_url'],
                                          cookies={'store_language': 'ru'},
                                          callback=self.parse)
            yield request

    def parse(self, response):
        item = War2022Team777Item()

        # Extracts the news_title and stores in scrapy item
        item['article_link'] = response.url
        item['article_uuid'] = hashlib.sha256(str(response.url).encode('utf-8')).hexdigest()
        item['article_id'] = response.url.split("/")[-1]
        item['article_datetime'] = response.xpath('//*[@id="_id_article"]/div[1]/div[1]/time/@datetime').extract()
        item['article_title'] = response.xpath('//*[@id="_id_article"]/div[1]/h1/text()').extract()
        item['article_text'] = "\n".join(response.xpath('//*[@id="_id_article"]/div[3]/span/text()').extract())
        item['article_author'] = "\n".join(response.xpath('//*[@id="_id_article"]/div[1]/div[2]/div[1]/span/span/a/@href').extract())

        yield (item)
