"/src/ai_scraper/settings.py"

## CONFIG FILE FOR SCRAPER

BOT_NAME = 'ai_scraper'  ## name
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"  ## gives bot user agent strings to behave like real one
ROBOTSTXT_OBEY = False   ## denies sections which are blocked by robots.txt file


## Playwright JS Handling
DOWNLOAD_HANDLERS = { 
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler"
} ## to handle downloads for pages with heavy JS

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor" ## handles async operaions with scrapy for efficient event handling

## Concurrency (config for 10k Pages/day === 7req/sec)
CONCURRENT_REQUEST = 16  ## number fo requests scrapy makes
AUTOTHROTTLE_ENABLE = True ## enables auto throttling for scrapers to adjust crawling speed based on server 
AUTOTHROTTLE_TARGET_CONCURRENCY = 8  ## target auto-throttle

## PostgreSQL pipeline
ITEM_PIPELINES = {
    "scraper.pipelines.PostgresPipeline": 300
} ## stores scraped data in database