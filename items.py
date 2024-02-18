import scrapy

class YourProjectNameItem(scrapy.Item):
    name = scrapy.Field()
    position = scrapy.Field()
    skills = scrapy.Field()
    linkedin_url = scrapy.Field()
