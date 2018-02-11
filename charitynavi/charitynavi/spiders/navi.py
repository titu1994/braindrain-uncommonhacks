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

        categories = response.xpath('//p[contains(@class, "crumbs")]/text()').extract_first()
        if categories is not None and ':' in categories:
            categories = categories.split(':')[0].strip()
        else:
            categories = 'Unknown'

        p_tags = response.xpath('//p/text()').extract()
        address_line1 = unicodedata.normalize('NFKD', p_tags[3]).strip()

        for i, line in enumerate(p_tags):
            if 'tel:' in line:
                phone = unicodedata.normalize('NFKD', line).replace('tel:', '').strip()
                address_line2 = unicodedata.normalize('NFKD', p_tags[i - 1]).strip()
                break
        else:
            phone = ""
            address_line2 = ""

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

        table_data = response.xpath('//td[contains(@align, "right")]/text()').extract()

        profit = self.clean_money(table_data[-2])

        fundraising_expenses = self.clean_money(table_data[-4])
        administrative_expenses = self.clean_money(table_data[-5])
        program_expenses = self.clean_money(table_data[-6])

        other_revenue = self.clean_money(table_data[-7])
        program_service_revenue = self.clean_money(table_data[-9])

        government_funds = self.clean_money(table_data[-11])
        related_organizations = self.clean_money(table_data[-12])
        fundraising_events = self.clean_money(table_data[-13])
        membership_dues = self.clean_money(table_data[-14])
        federated_campaigns = self.clean_money(table_data[-15])
        contributions = self.clean_money(table_data[-16])

        yield {
            'charity_name': charity_name,
            'category': categories,
            'address_line1': address_line1,
            'address_line2': address_line2,
            'phone': phone,
            'description': description,
            'overall_rating': overall_rating,
            'financial_rating': financial_rating,
            'transparency_rating': transparency_rating,
            'mission_statement': mission_statement,
            'profit': profit,
            'fundraising_expenses': fundraising_expenses,
            'administrative_expenses': administrative_expenses,
            'program_expenses': program_expenses,
            'other_revenue': other_revenue,
            'program_service_revenue': program_service_revenue,
            'government_funds': government_funds,
            'related_organizations': related_organizations,
            'fundraising_events': fundraising_events,
            'membership_dues': membership_dues,
            'federated_campaigns': federated_campaigns,
            'contributions': contributions,
        }

    def clean_money(self, ip):
        ip = unicodedata.normalize('NFKD', ip)
        ip = ip.replace("$", "")
        ip = ip.replace(",", "")
        ip = float(ip)
        return ip