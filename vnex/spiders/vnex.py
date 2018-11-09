import scrapy
import json
import re
from ..items import VnexItem

class scrape_vnexpress(scrapy.Spider):
	name = "scrape_vnexpress"

	start_urls=['https://vnexpress.net/tin-tuc/khoa-hoc/trong-nuoc/bo-truong-khoa-hoc-chinh-sach-chuyen-huong-de-khoa-hoc-gan-ket-thi-truong-3833275.html']
	
	def parse(self, response):
		# news = {}
		# news['title'] = response.xpath('//h1/text()|//h2/text()').extract()
		# news['content'] = response.xpath('//p[@class="Normal"]/text() | //p[@class="Normal"]/descendant::*/text()').extract()
		# with open('content.txt', 'w') as f:
		# 	f.write(json.dumps(news))
		# f.close()
		# with open('content.txt', 'r') as f:
		# 	print(json.loads(f.read()))
		title = response.xpath('//h1/text()|//h2/text()').extract()
		content = response.xpath('//p[@class="Normal"]/text() | //p[@class="Normal"]/descendant::*/text()').extract()
		category = response.xpath('//li[@class="start"]//descendant::a/text()').extract_first()
		item = VnexItem(title = title, category= category, content= content, url=response.url)
		links = response.xpath('//a[contains(@href,".html")]/@href').extract()
		# print(response.xpath('//li[@class="start"]//descendant::a/text()').extract_first())

		for link in links:
			l = response.urljoin(link)
			if re.search('vnexpress.net', l):
				if not re.search('vnexpress.net/tin-tuc/giao-duc/trac-nghiem', l):
					yield response.follow(link, callback=self.parse)
		yield item
