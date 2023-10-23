import logging

from BestSecretShop.credentials import EMAIL
from BestSecretShop.credentials import SECRET


class LoginPageScraper:

    logger = logging.getLogger(__name__)

    EMAIL = EMAIL
    SECRET = SECRET

    @classmethod
    async def accept_cookies(cls, response):

        page = response.meta["playwright_page"]

        await page.locator('css=button#cmp-accept-all').click()

    @classmethod
    async def login(cls, response):

        page = response.meta["playwright_page"]
        
        # await page.screenshot(path="LoginPage.png")

        await page.locator('css=input#login-username').click()
        await page.wait_for_timeout(500)
        
        await page.keyboard.type(cls.EMAIL, delay=100)
        await page.wait_for_timeout(500)

        await page.locator('css=input#j_password').click()
        await page.wait_for_timeout(500)

        await page.keyboard.type(cls.SECRET, delay=100)
        await page.wait_for_timeout(500)

        await page.keyboard.press("Enter", delay=100)

        try:
            await page.wait_for_selector('css=ul.header-icons')
            cls.logger.info("Login Succesfull.")
            # await page.screenshot(path="LoginSuccesfull.png")
        except:
            cls.logger.info("Login Failed.")
            # await page.screenshot(path="LoginFailed.png")
            raise Exception("Login Failed")

