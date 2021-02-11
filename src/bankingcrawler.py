import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request
import json

class BankingCrawler(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['https://www.moneycontrol.com/company-article/hdfcbank/news/HDF01']
    
    test = []

    def parse(self, response):
        PAGES_PATH = 'div.pages a::attr(href)'
        YEAR_SELECTOR = 'div.FR.yrs a::attr(href)'
        years_link = response.css(YEAR_SELECTOR).extract()[0:1]
        years_test = []
        for year in years_link:
            years_test.append('https://www.moneycontrol.com'+year)
        return (Request(url, callback=self.parse_manga_list_page) for url in years_test)

       
    def parse_manga_list_page(self, response):
        PAGES_PATH = 'div.pages a::attr(href)'
        pages_link = response.css(PAGES_PATH).extract()
        pages_test = []
        for page in pages_link:
            pages_test.append('https://www.moneycontrol.com'+page)
        pages_test.append('https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=HDF01&scat=&pageno=1&next=0&durationType=Y&Year=2021&duration=1&news_type=')
        return (Request(url, callback=self.content_parser) for url in pages_test)

    def content_parser(self,response):
        PAGES_PATH = 'div.FL.PR20 a::attr(href)'
        expanded = response.css(PAGES_PATH).extract()
        test = []
        for page in expanded:
            test.append('https://www.moneycontrol.com'+page)
        return (Request(url, callback=self.test_parse) for url in test)

    def test_parse(self,response):
        data = {}  
        data['title'] = response.css('h1::text').get()
        data['date'] = response.css('div.article_schedule span::text').get()
        data['time'] = response.css('div.article_schedule::text').getall()[1]
        data['content'] = response.css('div.content_wrapper p::text').getall()
        test.append(data)

    with open("/Users/krishnasharma/Desktop/hackerearth-hackathon-2021/data.json" , "a+") as outfile:
            json.dump(test, outfile) 
            
process = CrawlerProcess()
process.crawl(BankingCrawler)
process.start()