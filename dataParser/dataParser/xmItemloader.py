import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
class IndexLoader(ItemLoader):
    ''' indexLoader class body '''
    default_input_processor = TakeFirst()
    name_in = MapCompose(unicode.title)
    