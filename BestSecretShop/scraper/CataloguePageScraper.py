import logging
import datetime as dt
import json

from bs4 import BeautifulSoup


class CataloguePageScraper():

    logger = logging.getLogger(__name__)
    BASE_URL = "https://www.bestsecret.com"

    @classmethod
    async def get_HTML(cls, response):
        page = response.meta["playwright_page"]
        return await page.content()

    @classmethod
    async def get_catalogue_items(cls, response):
        page = response.meta["playwright_page"]
        soup = BeautifulSoup(await page.content(), "html.parser")
        catalogue_items = soup.find_all("div", {"class": "span product-container"})

        products_data = []
        for catalogue_item in catalogue_items:

            try:
                url = catalogue_item.find("a", {"class": "figure-image figure-image-hover"})["href"]

                split_url = url.split("&")
                for item in split_url:
                    if "code" in item:
                        code = item.split("=")[1]
                    if "colorCode" in item:
                        colorCode = item.split("=")[1]
                
                sku = f"{code}-{colorCode}"
                brand = catalogue_item.find("h3").text.replace("\n", "")
                description = catalogue_item.find("span", {"class": "product-desc"}).text

                uvp = catalogue_item.find("span", {"class": "t-value-old"}).text.split()
                if len(uvp) == 3:
                    ab_uvp = False
                else:
                    ab_uvp = True
                uvp = uvp[len(uvp)-1].replace(".", "").replace(",", ".")
                price = catalogue_item.find("span", {"class": "t-value t-highlight"}).text.split()
                if len(price) == 2:
                    ab_price = False
                else:
                    ab_price = True
                price = price[len(price)-1].replace(".", "").replace(",", ".")
                product_data = {
                    "crawl_date": str(dt.date.today()),
                    "crawl_url": page.url,
                    "product_url":"https://www.bestsecret.com/product.htm?&code={code}&colorCode={colorCode}".format(code=code, colorCode=colorCode),
                    "sku": sku,
                    "brand": brand,
                    "description": description,
                    "uvp": float(uvp),
                    "price": float(price),
                    "ab_uvp": ab_uvp,
                    "ab_price": ab_price
                }
                

                products_data.append(product_data)

            except AttributeError:
                cls.logger.error(f"Failed to scrape Product at {page.url}")
                continue

        return products_data

    @classmethod
    async def check_next_page(cls, response):
        page = response.meta["playwright_page"]
        soup = BeautifulSoup(await page.content(), "html.parser")

        if soup.find("div", {"class": "lipstick-pagination"}):

            cls.logger.debug("Found lipstick-pagination.")

            live_page = page.url
            next_page = cls.BASE_URL + soup.find("div", {"class": "lipstick-pagination"}).find_all("a")[-1]["href"]
            
            cls.logger.debug(f"Live Page: {live_page}")
            cls.logger.debug(f"Next Page: {next_page}")
            
            if live_page != next_page:
                return next_page
        
        return