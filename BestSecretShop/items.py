import scrapy

class CataloguePageFullShopItem(scrapy.Item):
    crawl_date = scrapy.Field()
    crawl_url = scrapy.Field()
    product_url = scrapy.Field()
    sku = scrapy.Field()
    brand = scrapy.Field()
    uvp = scrapy.Field()
    price = scrapy.Field()
    ab_uvp = scrapy.Field()
    ab_price = scrapy.Field()