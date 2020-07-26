# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhipinComItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pid = scrapy.Field()
    jobname = scrapy.Field()
    workyear = scrapy.Field()
    education_need = scrapy.Field()
    company_name = scrapy.Field()
    salary = scrapy.Field()
    company_industry = scrapy.Field()
    company_size = scrapy.Field()
    
    pass
