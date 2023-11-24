import scrapy

from BestSecretShop.items import CataloguePageFullShopItem

from BestSecretShop.scraper.LoginPageScraper import LoginPageScraper
from BestSecretShop.scraper.DesignerPageScraper import DesignerPageScraper
from BestSecretShop.scraper.CataloguePageScraper import CataloguePageScraper


from BestSecretShop.settings import CATALOGUE_PAGE_FULL_SHOP_OUTPUT_PATH

product_ids = {}
failed_urls = []

class CataloguePageFullShopSpider(scrapy.Spider):
    name = "CataloguePageFullShop"
    allowed_domains = ["bestsecret.com"]
    custom_settings = {
        'FEEDS': {
            CATALOGUE_PAGE_FULL_SHOP_OUTPUT_PATH: {'format': 'json', 'overwrite': True},
        },
        'ITEM_PIPELINES': {
            "BestSecretShop.pipelines.SaveToMySQLPipeline_CataloguePageFullShop": 100,
            "BestSecretShop.pipelines.UploadToBlobStorage_CataloguePageFullShop": 200,
        },
        'DOWNLOAD_HANDLERS' : {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        }
    }


    def start_requests(self):
        
        yield scrapy.Request(
            url = 'https://www.bestsecret.com/entrance/index.htm',
            callback=self.parse_login_page,
            errback=self.errback_close_page,
            meta={
                "playwright": True,
                "playwright_include_page": True,
            }
        )

    # def start_requests(self):
        
    #     yield scrapy.Request(
    #         url = 'https://www.bestsecret.com/entrance/index.htm',
    #         callback=self.test_parse_catalogue,
    #         errback=self.errback_close_page,
    #         meta={
    #             "playwright": True,
    #             "playwright_include_page": True,
    #         }
    #     )

    async def test_parse_catalogue(self, response):
        await LoginPageScraper.accept_cookies(response)
        await LoginPageScraper.login(response)

        page = response.meta["playwright_page"]
        await page.close()

        url = "https://www.bestsecret.com/designer_shop_category.htm?shop=label_3569&gender=MALE&back_url=/designer.htm&back_param_gender=MALE"
        self.logger.info(f"Request: {url}")
            
        try: 
            yield scrapy.Request(
                url = url,
                callback = self.parse_catalogue_page,
                errback=self.errback_close_page,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                }
            )
        except Exception:
            self.logger.error(f"Request ERROR: {url}")

        page = response.meta["playwright_page"]
        await page.close()


    async def parse_login_page(self, response):
        
        await LoginPageScraper.accept_cookies(response)
        await LoginPageScraper.login(response)

        self.logger.info("########################################")
        self.logger.info("####### Start getting Campaigns. #######")

        designer_by_gender = [
            'https://www.bestsecret.com/designer.htm?gender=FEMALE&storeGender=true',
            'https://www.bestsecret.com/designer.htm?gender=MALE&storeGender=true',
            'https://www.bestsecret.com/designer.htm?gender=KIDS&storeGender=true'
        ]
        for gender_url in designer_by_gender:
            self.logger.debug(f"Request: {gender_url}")
            yield scrapy.Request(
                url = gender_url,
                callback=self.parse_designer_page,
                errback=self.errback_close_page,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                },
            )

        page = response.meta["playwright_page"]
        await page.close()

        # self.logger.info(failed_urls)
        # self.logger.info(f"Anzahl failed URLs: {len(failed_urls)}")
        # self.logger.info(f"Anzahl verschiedener CVs: {len(product_ids)}")
        

    async def parse_designer_page(self, response):
        designer_urls = await DesignerPageScraper.get_designer(response)

        self.logger.info(f"Number of Designer: {len(designer_urls)}")

        for url in designer_urls:

            self.logger.debug(f"Request: {url}")
            
            try: 
                yield scrapy.Request(
                    url = url,
                    callback = self.parse_catalogue_page,
                    # errback=self.errback_close_page,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                    }
                )
            except Exception:
                self.logger.error(f"Request ERROR: {url}")
                failed_urls.append(url)

        page = response.meta["playwright_page"]
        await page.close()


    async def parse_catalogue_page(self, response):

        self.logger.info("########################################")
        self.logger.info("##### Start getting CataloguePage. #####")


        while True:

            # try:
            catalogue_products, soup = await CataloguePageScraper.get_catalogue_items(response)
            # except Exception as e:
            #     self.logger.error("WARNING - Page could not be loaded!")
            #     self.logger.error(e)
            #     page = response.meta["playwright_page"]
            #     await page.close()
            #     break
        
            for prod in catalogue_products:
                
                if prod['sku'] in product_ids.keys():
                    self.logger.info(
                        f'Product({prod["sku"]}) is already scraped. \nFirts scrape at: {product_ids[prod["sku"]]} \nSecond: {prod["crawl_url"]}'
                    )
                    continue
                else:
                    product_ids[prod["sku"]] = prod["crawl_url"]

                item = CataloguePageFullShopItem()
                item["crawl_date"] = prod["crawl_date"]
                item["crawl_url"] = prod["crawl_url"]
                item["product_url"] = prod["product_url"]
                item["sku"] = prod["sku"]
                item["brand"] = prod["brand"]
                item["uvp"] = prod["uvp"]
                item["price"] = prod["price"]
                item["ab_uvp"] = prod["ab_uvp"]
                item["ab_price"] = prod["ab_price"]
                
                yield item

            check = await CataloguePageScraper.check_next_page(response, soup)
            self.logger.info(f"NextPage: {check}")

            page = response.meta["playwright_page"]
            if check:
                await page.goto(check)
            else:
                await page.close()
                break


    async def errback_close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
