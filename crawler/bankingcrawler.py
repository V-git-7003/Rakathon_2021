import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request
import json
import os
import logging
import test as tp

class BankingCrawler(scrapy.Spider):
    name = "Bank_Crawler"
    
    start_urls = ['https://www.moneycontrol.com/company-article/indusindbank/news/IIB']

    def __init__(self, bank_id="",updated_path=""):
        self.bank_id=bank_id
        self.updated_path=updated_path

    def parse(self, response):
        cwd = os.getcwd()
        path_of_dir = format(cwd)
        new_path = path_of_dir.replace("/src","/files")
        self.updated_path=new_path
        PAGES_PATH = 'div.pages a::attr(href)'
        YEAR_SELECTOR = 'div.FR.yrs a::attr(href)'
        years_link = response.css(YEAR_SELECTOR).extract()[0:10]
        years_test = []
        for year in years_link:
            years_test.append('https://www.moneycontrol.com'+year)
        return (Request(url, callback=self.page_parser) for url in years_test)

       
    def page_parser(self, response):
        PAGES_PATH = 'div.pages a::attr(href)'
        pages_link = response.css(PAGES_PATH).extract()
        current_page = str(response.css("div.pages.MR10.MT15 span b::text").get())
        pages_test = []
        current_ = ""
        for page in pages_link:
            start_page = 0
            if (page.find('pageno')>-1) : 
                start = int(page.index('pageno'))
                equal_length = int(len('pageno'))
                end = int(start+equal_length+2)
                current_ = page[start:end]
            pages_test.append('https://www.moneycontrol.com'+page)

        current_doc = 'https://www.moneycontrol.com' + pages_link[0].replace(current_,"pageno="+current_page)
        pages_test.append(current_doc)
        return (Request(url, callback=self.link_parser) for url in pages_test)

    def link_parser(self,response):
        this = "h1.b_42.PT20::text"
        title = response.css(this).get()
        self.bank_id = title.split()[0]
        PAGES_PATH = 'div.FL.PR20 a::attr(href)'
        expanded = response.css(PAGES_PATH).extract()
        test = []
        for page in expanded:
            test.append('https://www.moneycontrol.com'+page)
        return (Request(url,callback=self.content_parser) for url in test)

    
    def content_parser(self,response):
        bank = self.bank_id
        date = response.css('div.article_schedule span::text').get()
        if  (date and not date.isspace()):
            data = {}
            data[bank] = []
            data[bank].append({
                'title': response.css('h1::text').get(),
                'date': date,
                'time': 'None' if len(response.css('div.article_schedule::text'))<2 else  response.css('div.article_schedule::text').getall()[1],
                'content': response.css('div.content_wrapper p::text').getall()
            })
            news = {} 
            updated_path = self.updated_path+"/"+bank+".json"

            if not os.path.exists(updated_path):
                with open(updated_path, 'w') as outfile: 
                    json.dump(news,outfile)

            with open(updated_path) as outfile:
                news = json.load(outfile)
             
            if bank not in news:
                news=data
            else:
                news[bank].append({
                    'title': response.css('h1::text').get(),
                    'date': date,
                    'time': 'None' if len(response.css('div.article_schedule::text'))<2 else  response.css('div.article_schedule::text').getall()[1],
                    'content': response.css('div.content_wrapper p::text').getall()
                    })
            with open(updated_path, "w+") as outfile:
                json.dump(news,outfile)
            print("done")
        else:
            print("The record misses dates for following -->" , response.url)

def updloadfile(bucket_name):
    try:
        tp.upload_file("test-krishna-tbd-1")
    except Exception as e:
        logging.error(e)
        return False
    return True
    
process = CrawlerProcess()
process.crawl(BankingCrawler)
process.start()

print("uploaded to file --> ",updloadfile("s3_bucket_name"))
