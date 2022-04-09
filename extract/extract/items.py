# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ExtractItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Staple(scrapy.Item):
    name = scrapy.Field()
    mana_cost = scrapy.Field()
    percentage_deck = scrapy.Field()
    played_number = scrapy.Field()
    image = scrapy.Field()
    format = scrapy.Field()
    type = scrapy.Field()
