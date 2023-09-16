import logging

from bs4 import BeautifulSoup


class DesignerPageScraper:

    logger = logging.getLogger(__name__)
    BASE_URL = "https://www.bestsecret.com"
    
    @classmethod
    async def get_designer(cls, response):

        page = response.meta["playwright_page"]

        await page.wait_for_selector('css=input#designer-search')
        await page.wait_for_selector('css=div#A')
        await page.wait_for_selector('css=div#Z')
        
        # await page.screenshot(path="DesignerPage.png", full_page=True)

        soup = BeautifulSoup(await page.content(), 'html.parser')

        designer = soup.find_all("a", {"class": "designer-tile-link"})

        designer_urls = []
        for a in designer:
            designer_urls.append(cls.BASE_URL + a["href"])

        return designer_urls


        
        

        
