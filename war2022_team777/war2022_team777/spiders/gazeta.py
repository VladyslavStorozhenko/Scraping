import scrapy
from ..items import War2022Team777Item


class GazetaSpider(scrapy.Spider):
    name = 'gazeta'
    allowed_domains = ['m.gazeta.ru']
    start_urls = ['https://m.gazeta.ru/politics/news/',
                  'https://m.gazeta.ru/business/news/',
                  'https://m.gazeta.ru/army/news/',
                  ]

    def start_requests(self):
        for link_url in self.start_urls:
            print(link_url)
            # Request to get the HTML content
            request = scrapy.http.Request(link_url, cookies={'store_language': 'ru'}, callback=self.parse)
            yield request

    def parse(self, response):
        # print("\n")
        # print("HTTP STATUS: " + str(response.status))
        # print(response.xpath("//h2/a/text()").get())
        # print("\n")
        item = War2022Team777Item()
        # Gets HTML content where the article links are stored
        content = response.xpath('/html/body/div[10]')
        # Loops through the each and every article link in HTML 'content'
        for article_link in content.xpath('.//a'):
            # Extracts the href info of the link to store in scrapy item
            item['article_url'] = article_link.xpath('.//@href').extract_first()
            if item['article_url'].startswith("http") or 'photo' in item['article_url']:
                continue
            item['article_url'] = "https://" + self.allowed_domains[0] + item['article_url']
            print(item['article_url'])
            yield (item)
