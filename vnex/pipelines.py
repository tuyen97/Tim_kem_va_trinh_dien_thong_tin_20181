from scrapy.exceptions import DropItem
import json

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['title'][0] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['title'][0])
            return item

class NoneFilterPipeline(object):

	def process_item(self, item, spider):
		if item['title'] is not None and item['content'] is not None and item['category'] is not None:
			if len(item['title']) == 0 or len(item['content'])==0 or len(item['category'])==0:
				raise DropItem('item not valid')
			else:
				return item
		else:
			raise DropItem('item not valid')

class WriteJsonPipeline(object):
	def open_spider(self, spider):
		self.file = open('items.jl', 'w')

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + "\n"
		self.file.write(line)
		return item
