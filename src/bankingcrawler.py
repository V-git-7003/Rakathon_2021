import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request
import json
import os
import logging

class BankingCrawler(scrapy.Spider):
    name = "brickset_spider"
    
    start_urls = ['https://www.moneycontrol.com/company-article/indusindbank/news/IIB']

    def __init__(self, temp="",updated_path=""):
        self.temp=temp
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
        return (Request(url, callback=self.parse_bank_list) for url in years_test)

       
    def parse_bank_list(self, response):
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
        return (Request(url, callback=self.content_parser) for url in pages_test)

    def content_parser(self,response):
        this = "h1.b_42.PT20::text"
        title = response.css(this).get()
        self.temp = title.split()[0]
        PAGES_PATH = 'div.FL.PR20 a::attr(href)'
        expanded = response.css(PAGES_PATH).extract()
        test = []
        for page in expanded:
            test.append('https://www.moneycontrol.com'+page)
        return (Request(url,callback=self.test_parse) for url in test)

    #TODO create exponential back off 
    def test_parse(self,response):
        self_temp = self.temp
        date = response.css('div.article_schedule span::text').get()
        if(not (not (date and not date.isspace()))):
            data = {}
            data[self_temp] = []
            data[self_temp].append({
                'title': response.css('h1::text').get(),
                'date': date,
                'time': 'None' if len(response.css('div.article_schedule::text'))<2 else  response.css('div.article_schedule::text').getall()[1],
                'content': response.css('div.content_wrapper p::text').getall()
            })
            test_object = {} 
            updated_path = self.updated_path+"/"+self_temp+".json"

            if not os.path.exists(updated_path):
                with open(updated_path, 'w') as outfile: 
                    json.dump(test_object,outfile)

            with open(updated_path) as outfile:
                test_object = json.load(outfile)
             
            if self_temp not in test_object:
                test_object=data
            else:
                test_object[self_temp].append({
                    'title': response.css('h1::text').get(),
                    'date': date,
                    'time': 'None' if len(response.css('div.article_schedule::text'))<2 else  response.css('div.article_schedule::text').getall()[1],
                    'content': response.css('div.content_wrapper p::text').getall()
                    })
            with open(updated_path, "w+") as outfile:
                json.dump(test_object,outfile)
            print("done")
        else:
            print("The record misses dates for following -->" , response.url)

process = CrawlerProcess()
process.crawl(BankingCrawler)
process.start()