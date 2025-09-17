import scrapy
import pandas as pd

class PriceSpider(scrapy.Spider):
    name = "price_spider"
    start_urls = ["https://www.ebay.com/sch/i.html?_nkw=laptop"]  # Sample: eBay laptops

    def parse(self, response):
        for product in response.css("div.s-item"):
            yield {
                "name": product.css("div.s-item__title::text").get(),
                "price": float(product.css("span.s-item__price::text").get().replace("$", "")),
                "timestamp": pd.Timestamp.now()
            }

# Run: scrapy crawl price_spider -o data/competitor_prices.json