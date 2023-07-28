import scrapy


class NewsspiderSpider(scrapy.Spider):
    name = "newsspider"
    allowed_domains = ["nepalitimes.com"]
    start_urls = ["https://nepalitimes.com"]

    def parse(self, response):
        pass
