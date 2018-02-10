import scrapy
import unicodedata

class CharityNavigatorSpider(scrapy.Spider):
    name = 'charitynav'

    def start_requests(self):
        baseurl = 'https://www.yelp.com/biz/'
        for name in all_restaurant_names:
            path = name.lower().split()  # get actual words of the restaurant name
            path = '-'.join(path)  # join wiht - as required
            url = path + '-chicago'  # append chicago to enforce searching for business in chicago only

            yield scrapy.Request(baseurl + url, callback=self.parse)

    def parse(self, response):
        restaurant = response.url[25:].split('-')
        restaurant_name = ' '.join(restaurant[:-1])

        response.selector.remove_namespaces()

        ratings = response.xpath('//div[contains(@class, "i-stars")]/@title').extract()
        reviews_ = response.xpath("//p[contains(@lang, 'en')]").extract()

        self.logger.info("Restaurant Name" + restaurant_name + ": Number of ratings = " + str(len(ratings)))

        for i, (rating, review_para) in enumerate(zip(ratings, reviews_)):
            # clean rating
            rating = int(rating[0])

            review_para = review_para[13:-4]  # remove the <p > </p> parts
            review_para = review_para.replace('<br>', '')  # replace new lines and breaks

            # Ref: https://stackoverflow.com/questions/10993612/python-removing-xa0-from-string
            review = unicodedata.normalize('NFKD', review_para)

            item = {
                'restaurant_name': restaurant_name,
                'review': review,
                'rating': rating
            }
            yield item

        current_page = response.xpath("//div[contains(@class, 'page-of-pages')]/text()").extract_first()

        if current_page is not None:
            current_page = current_page.replace('\n', '').strip().split()
            current_idx = int(current_page[1])
            total_idx = int(current_page[-1])

            if current_idx + 1 <= total_idx:
                start_count = 20 * (current_idx + 1)

                baseurl = response.url[:25]
                name = restaurant_name.split()
                name = '-'.join(name)
                name = name + '-chicago?start=%d' % start_count
                url = baseurl + name

                message = 'restaurant = ' + restaurant_name + ' | following next page to ' + url
                self.logger.info(message)

                if url is not None:
                    yield scrapy.Request(url, callback=self.parse)
