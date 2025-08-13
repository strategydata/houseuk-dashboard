import logging

from scrapy.spiders import SitemapSpider
from scrapy.http import Request, Response
from scrapy.spiders.sitemap import iterloc
from collections.abc import Iterable
from scrapy.loader import ItemLoader
from scrapy_selenium import SeleniumRequest
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots

from house.extract.rightmove.rightmove.items import RightmoveItem

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RightmoveSpider(SitemapSpider):
    """
    rightmove
    """

    name = "rightmove"

    sitemap_urls = ["https://www.rightmove.co.uk/sitemap.xml"]
    sitemap_rules = [
        (r"/properties/\d+", "parse"),
    ]

    def _parse_sitemap(self, response: Response) -> Iterable[Request]:
        if response.url.endswith("/robots.txt"):
            for url in sitemap_urls_from_robots(response.text, base_url=response.url):
                yield Request(url, callback=self._parse_sitemap)
        else:
            body = self._get_sitemap_body(response)
            if body is None:
                logger.warning(
                    "Ignoring invalid sitemap: %(response)s",
                    {"response": response},
                    extra={"spider": self},
                )
                return
            s = Sitemap(body)
            it = self.sitemap_filter(s)
            if s.type == "sitemapindex":
                for loc in iterloc(it, self.sitemap_alternate_links):
                    if any(x.search(loc) for x in self._follow):
                        yield Request(loc, callback=self._parse_sitemap)
            elif s.type == "urlset":
                for loc in iterloc(it, self.sitemap_alternate_links):
                    for r, c in self._cbs:
                        if r.search(loc):
                            yield SeleniumRequest(url=loc, callback=c)
                            break

    def parse(self, response):
        loader = ItemLoader(item=RightmoveItem(), response=response)
        loader.add_xpath("url", '//link[@rel="canonical"]/@href')
        loader.add_xpath("price", "//article/div/div/div/span[1]/text()")
        loader.add_xpath("title", "//h1/text()")
        loader.add_xpath("property_type", "//article/dl/div[1]/dd/span/p/text()")
        loader.add_xpath("bedrooms", "//article/dl/div[2]/dd/span/p/text()")
        loader.add_xpath("bathrooms", "//article/dl/div[3]/dd/span/p/text()")
        loader.add_xpath("size", "//article/dl/div[4]/dd/span/p/text()")
        loader.add_xpath("tenure", "//article/dl/div[5]/button/div/dd/span/p/text()")
        loader.add_xpath("feature", "//h2/following-sibling::ul/text()")
        loader.add_xpath("description", "//h2/following-sibling::div/div/text()")
        loader.add_xpath("council_tax", "//article[3]/dl/div[1]/dd/text()")
        loader.add_xpath("parking", "//article[3]/dl/div[2]/dd/text()")
        loader.add_xpath("garden", "//article[3]/dl/div[3]/dd/text()")
        loader.add_xpath("accessibility", "//article[3]/dl/div[4]/dd/text()")
        loader.add_xpath("latitude", "//h2/following-sibling::div/div/a/img/@src")
        loader.add_xpath("longitude", "//h2/following-sibling::div/div/a/img/@src")
        loader.add_xpath("phone", "//a[starts-with(@href, 'tel:')]/@href")
        loader.add_xpath(
            "image_urls",
            "//a[@rel=\"nofollow\"]/img[starts-with(@src, 'https://media.rightmove.co.uk')]/@src",
        )
        yield loader.load_item()
