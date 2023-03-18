import scrapy
import unicodedata
import re
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.item import Item, Field


char = (chr(i) for i in range(0x110000))
control = "".join(i for i in char if unicodedata.categroy(i) == "Cc")
re_control = re.compile("[%s]" % re.escape(control))


class Link(Item):
    source_url = Field()
    target_url = Field()
    target_document = Field()


class AuthorityScore(Item):
    SHA_hash_url = Field()
    pagerank_score = Field()
