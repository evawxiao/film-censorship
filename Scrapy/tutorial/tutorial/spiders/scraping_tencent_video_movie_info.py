# This script scrapes all US videos off Tencent Video.

# To run this Scrapy spider, make sure you have Scrapy installed (https://docs.scrapy.org/en/latest/).
# Run command: scrapy crawl tencentvideo -o tencent_video.json

import scrapy
import re
import csv

class TencentVideoSpider(scrapy.Spider):
	name = 'tencentvideo'
	start_urls =  ['http://v.qq.com/x/list/movie?iarea=3&offset=0']

	def parse(self, response):

		videos_root_URL ="http://v.qq.com/x/list/movie"
		list_of_movies = response.xpath('//strong[@class="figure_title"]/a/@href').extract() 
		
		# iterate through all movie links on page
		for href in list_of_movies:
			yield response.follow(href, self.parse_movie)

		next_page = response.xpath('//a[@class="page_next"]/@href').extract_first()
		next_page = videos_root_URL + next_page

		# iterate through movie list pagination
		if next_page != None:
			yield response.follow(next_page, self.parse)

	def parse_movie(self, response):

		yield {
			'chinese_title': response.xpath('//div[@class="tit"]/text()').extract_first(),
			'english_title': response.xpath('//span[@class="alias"]/text()').extract_first(),
			'china_runtime': response.xpath('//div[@class="figure_count"]/span[@class="num"]/text()').extract_first(), 
			'china_release_date': response.xpath('//meta[@itemprop="datePublished"]/@content').extract_first(),
		}
		
