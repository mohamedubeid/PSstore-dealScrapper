import scrapy
from scrapy.item import Item, Field

class PsspiderItem(Item):
    url = Field()
    name = Field()
    AfterCut = Field()
    OGprice = Field()