from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scraper.items import ScraperItem

def baseUrl():
    url = "https://sfbay.craigslist.org/search/zip?query=mattress&hasPic=1&searchNearby=2"
    areas = [63,187,43,373,709,189,454,285,96,102,188,92,12,191,62,710,708,97,707,346,456]
    areasQ = "".join(map( lambda area: "&nearbyArea={0}".format(area), areas))
    return url+areasQ

class ListSpider(CrawlSpider):
    name = "list"
    allowed_domains = ["craigslist.org"]
    start_urls = [ baseUrl() ]

    rules = [
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse_items", follow= True),
    ]

    def parse_start_url(self, response):
        return self.parse_items(response)

    def parse_items(self, response):
        rows = Selector(response).xpath("//p[@class='row']")
        items = []
        for row in rows:
            item = ScraperItem()
            item["title"] = row.xpath(".//span[@class='pl']/a/span/text()").extract()
            item["link"] = row.xpath(".//span[@class='pl']/a/@href").extract()
            items.append(item)
        return items

