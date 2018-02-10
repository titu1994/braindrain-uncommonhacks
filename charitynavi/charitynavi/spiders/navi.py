import scrapy
import unicodedata

class CharityNavigatorSpider(scrapy.Spider):
    name = 'charitynav'

    def start_requests(self):
        baseurl = 'https://www.charitynavigator.org/index.cfm?FromRec=%d&keyword_list=&bay=search.results&EIN=&cgid=&cuid=&location=2&state=IL&city=&overallrtg=&size=&scopeid=&ratingstatus=rated'

        for i in range(0, 325, 20):
            yield scrapy.Request(baseurl % i, callback=self.go_to_charity)

    def go_to_charity(self, response):
        response.selector.remove_namespaces()

        charity_links = response.xpath('//h3[contains(@class, "charity-name-desktop")]/a/@href').extract()

        for link in charity_links:
            yield response.follow(link, callback=self.parse_charity)

    def parse_charity(self, response):
        response.selector.remove_namespaces()

        charity_name = response.xpath('//h1[contains(@class, "charityname")]/text()').extract_first()
        charity_name = charity_name.replace('\n', '').strip()

        description = response.xpath('//h2[contains(@class, "tagline")]/text()').extract_first()
        if description is not None and len(description) != 0:
            description = description.strip()
        else:
            description = ""

        ratings_ = response.xpath('//td[contains(@align, "center")]/text()').extract()
        try:
            overall_rating = float(ratings_[0])
        except:
            overall_rating = -1

        try:
            financial_rating = float(ratings_[1])
        except:
            financial_rating = -1

        try:
            transparency_rating = float(ratings_[2])
        except:
            transparency_rating = -1

        mission_statement = response.xpath('//div[contains(@class, "accordion-item-bd")]/p/text()').extract_first()
        if mission_statement is not None and len(mission_statement) != 0:
            mission_statement = mission_statement.strip()
        else:
            mission_statement = ""

        yield {
            'charity_name': charity_name,
            'description': description,
            'overall_rating': overall_rating,
            'financial_rating': financial_rating,
            'transparency_rating': transparency_rating,
            'mission_statement': mission_statement,
        }