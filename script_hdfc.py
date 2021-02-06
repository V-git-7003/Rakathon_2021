import scrapy

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['https://www.moneycontrol.com/company-article/hdfcbank/news/HDF01']

    def parse(self, response):
        SET_SELECTOR = 'div.MT15'
        for div_classes in response.css(SET_SELECTOR):
         
              NAME_SELECTOR = 'a::attr(href)'
              yield {'name':div_classes.css(NAME_SELECTOR).extract_first()
              }


 #response.css('div.MT15 a::attr(href)').extract_first()      
