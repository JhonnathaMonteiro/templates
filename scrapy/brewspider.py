# -*- coding: utf-8 -*-
"""
Spider Example using xpath
"""
import scrapy


class BrewspiderSpider(scrapy.Spider):
    name = 'brewspider'
    allowed_domains = ['www.beeradvocate.com']
    start_urls = ['http://www.beeradvocate.com/beer/styles/']

    def parse(self, response):
        # follow the bear style pages
        for href in response.xpath('//*[@class="stylebreak"]/ul/li/a/@href').getall():
            yield response.follow(href, self.parse_bears)

    def parse_bears(self, response):
        # page follow
        for href in response.xpath('//*[@id="ba-content"]/table/tr[position()>3 and last()-1]/td[1]/a/@href').getall():
            yield response.follow(href, self.parse_bear)

        # TODO: write a follow to pagination
        # for href bla bla bla...

    def parse_bear(self, response):
        yield {
            'teste': response.xpath('//*[@id="info_box"]/a[1]/b').get(),
        }
