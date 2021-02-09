import scrapy
from scrapy import Request
class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['https://www.moneycontrol.com/company-article/hdfcbank/news/HDF01']
    
    def parse(self, response):
        xp = 'div.pages a::attr(href)'

        temp_list = []

        for a_class in response.css(xp).extract():
            temp_list.append("https://www.moneycontrol.com"+a_class)
        
        st_url = 'https://www.moneycontrol.com/company-article/hdfcbank/news/HDF01'
        temp_list.append(st_url)
        
        print("temp list ",temp_list,'Length of the list',len(temp_list))
        
        return (Request(url, callback=self.parse_manga_list_page) for url in temp_list)
       
    
    def parse_manga_list_page(self, response):
        SET_SELECTOR = 'div.MT15'
        for div_classes in response.css(SET_SELECTOR):
              NAME_SELECTOR = 'a::attr(href)'
              print('name', div_classes.css(NAME_SELECTOR).extract_first())
              print()
               


