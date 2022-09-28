import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

			
    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                'text': quote.xpath("span[@class='text']/text()").extract(),
                'author': quote.xpath("span/small[@class='author']/text()").extract(),
                'tags': quote.xpath("div[@class='tags']//a[@class='tag']/text()").extract(),
            }
        next_page = response.xpath("//li[@class='next']/a/@href").extract()
        if next_page is not None:
            next_page = response.urljoin(next_page[0])
            yield scrapy.Request(next_page, callback=self.parse)