import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from utils.selectors import load_site_config
from utils.auth import login

class UniversalSpider(scrapy.Spider):
    name = "universal"
    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE":"chromium"
    }

    def __init__(self, domain, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = domain
        self.config = load_site_config(domain)
        self.start_urls = [self.config.get("start_url", f"https://{domain}")]
        self.link_extractor = LinkExtractor(allow_domains= [domain])

    def start_requests(slef):
        if self.config.get("login_required"):
            cookies = login(self.domain)
            for url in self.start_urls:
                yield Request(url, cookies=cookies, callback=self.parse)
        else:
            yield from super().start_requests()

    def parse(self, response):
        item = {
            'domain':self.domain,
            'url':response.url,
            'title':response.css(slef.config['selectors']['title']).get(),
            'content':" ".join(response.css(self.config['selectors']['content']).get_all())
        }
        if "date" in self.config['selectors']:
            item['published_date'] = response.css(self.config['selectors']['date']).get()

        yield item

        for link in self.link_extractor.extract_links(response):
            yield Request(link.url, callback=self.parse)
            