import scrapy
from scrapy import Request
import time

class BankParse(scrapy.Spider):
    name = "bank_parser"
    start_urls = ['https://www.moneycontrol.com/company-article/statebankindia/news/SBI']
    
    def parse(self, response):
        PAGES_PATH = 'div.pages a::attr(href)'
        YEAR_SELECTOR = 'div.FR.yrs a::attr(href)'
        
          
        years_link = response.css(YEAR_SELECTOR).extract()[0:7]
        time.sleep(3)
        #print(years_link)
        print('\n Years:')  
        years_link = ["https://www.moneycontrol.com"+ year for year in years_link] #concatinating for full list
        print(years_link)
        
        return (Request(year,callback=self.page_parser) for year in years_link)
    
  
    def page_parser(self, response):
        #SET_SELECTOR = 'div.MT15'
        PAGES_PATH = 'div.pages a::attr(href)'
        #YEAR_SELECTOR = 'div.FR.yrs'
        time.sleep(1)
        pages_link = response.css(PAGES_PATH).extract()

        #print('\n Pages:')
        pages_link = ["https://www.moneycontrol.com"+page for page in pages_link]
        print(pages_link)
        print('\n'*4)
        return (Request(page,callback=self.content_parser) for page in pages_link)   
   
    def content_parser(self,response):
       #TITLE_PATH = 'h1::text'
       print('\n*2 new page:')
       time.sleep(2)
       yield {'title':response.css('h1::text').get(),
              'date':response.css('div.article_schedule span::text').get(), 
              'time':response.css('div.article_schedule::text').getall()[1],
              'content':response.css('div.content_wrapper p::text').getall() 
              }  



