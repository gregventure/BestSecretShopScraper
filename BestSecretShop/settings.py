# Scrapy settings for BestSecretShop project

import datetime as dt


BOT_NAME = "BestSecretShop"

SPIDER_MODULES = ["BestSecretShop.spiders"]
NEWSPIDER_MODULE = "BestSecretShop.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de",
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'BestSecretShop.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 100,
    # 'BestSecretShop.middlewares.ScrapeOpsFakeUserAgentMiddleware': 100,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 2
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 10.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# ------------------------------------------------------------------------------- #
#                               Custom Settings                                   #
# ------------------------------------------------------------------------------- #

LOG_LEVEL = 'INFO'

# ------------------------------------------------------------------------------- #

# Generate Different Headers from ScrapeOps API
SCRAPEOPS_API_KEY = '7fdce0bf-ae4e-4769-ba3f-bf1400bcde87'
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 5

# ------------------------------------------------------------------------------- #

DATE = str(dt.date.today()).replace("-", "_")

# MySQLDatabase

MYSQL_CATALOGUE_PAGE_FULL_SHOP_DB = 'BestSecret_Scraping'
MYSQL_CATALOGUE_PAGE_FULL_SHOP_TB = f'CATALOGUE_PAGE_FULL_SHOP_{DATE}'

# ------------------------------------------------------------------------------- #

# CataloguePageFullShop
CATALOGUE_PAGE_FULL_SHOP_OUTPUT_PATH = f'data/{dt.date.today()}_CATALOGUE_PAGE_FULL_SHOP.json'
CATALOGUE_PAGE_FULL_SHOP_LOCALPATH = 'data/CATALOGUE_PAGE_FULL_SHOP.json'
CATALOGUE_PAGE_FULL_SHOP_DEST_BLOB = f'CATALOGUE_PAGE_FULL_SHOP_{dt.date.today()}'

# ------------------------------------------------------------------------------- #

# Retry Failed Http Request
# RETRY_HTTP_CODES = [403]
# RETRY_TIMES = 5

# ------------------------------------------------------------------------------- #


PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "timeout": 20 * 1000,  # 20 seconds
}

PLAYWRIGHT_CONTEXTS = {

    "default": {
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0",
    }
}

PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 10

PLAYWRIGHT_PROCESS_REQUEST_HEADERS = None