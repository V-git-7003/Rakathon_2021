import scrapy
import constants
import utils
from scrapy import Request

class BankingCrawler(scrapy.Spider):
    name = constants.name
    start_urls = utils.nifty_fifty_urls_from_properties(constants.file_name)

    def parse(self, response):
        div_pages = constants.div_pages+constants.space+constants.href
        urls = []
        for a_class in response.css(div_pages).extract():
            urls.append("https://www.moneycontrol.com"+a_class)
        urls.append(constants.current_page)
        
        #replace all print with logger.debug
        print("temp list ",temp_list,'Length of the list',len(temp_list))
        
        return (Request(url, callback=self.parse_manga_list_page) for url in temp_list)
       
    
    def parse_manga_list_page(self, response):
        SET_SELECTOR = 'div.MT15'
        for div_classes in response.css(SET_SELECTOR):
              NAME_SELECTOR = 'a::attr(href)'
              print('name', div_classes.css(NAME_SELECTOR).extract_first())
              print()