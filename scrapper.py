import scrapy
from scrapy.crawler import CrawlerProcess
import json
import os


class ScrapperSpider(scrapy.Spider):
    """Scrapes a static page.
    Finds Screen size and number of usb ports.
    """

    name = "ScrapperSpider"
    start_urls = [
        'https://www.hembiobutiken.se/produkter/tv-apparater/77-tum/329910-philips-77oled806-12/'
    ]

    def parse(self, response):
        selector = response.xpath('//div[@class = "row produktspec"]')
        screen_size = selector.xpath(
                '//p[contains(text(),"Bildyta")]/b/text()'
            ).get()
        usb_count = selector.xpath(
                '//p[contains(text(),"anslutningar")]/b/text()'
            ).get().split(' ')[0]

        yield {'Screen Size': screen_size, 'USB Count': usb_count}



if __name__ == "__main__":
    jsonfile = r'./value.json'

    if os.path.isfile(jsonfile):
        os.unlink(jsonfile)

    process = CrawlerProcess(settings={
        "FEEDS": {
            jsonfile: {"format": "json"},
        },
    })
    process.crawl(ScrapperSpider)
    process.start()

    with open(jsonfile, 'r') as jsonfd:
        values = json.load(jsonfd)
        print(values[0])

