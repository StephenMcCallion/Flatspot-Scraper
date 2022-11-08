import scrapy

class FlatspotSpider(scrapy.Spider):
    name = 'flatspot'
    start_urls = ['https://rollersnakes.co.uk/collections/mens-clothing?filter.v.availability=1&page=1']

    def parse(self, response):
        for products in response.css('div.ProductItem'):
            try:
                yield {
                    'name': products.css('h2.ProductItem__Title a::text').get(),
                    'price': products.css('div.ProductItem__PriceList span::text').get().replace('£', ''),
                    'link': 'https://rollersnakes.co.uk' + products.css('h2.ProductItem__Title a').attrib['href']
                }
            except:
                yield {
                    'name': products.css('h2.ProductItem__Title a::text').get(),
                    'price': 'not on offer',
                    'link': 'https://rollersnakes.co.uk' + products.css('h2.ProductItem__Title a').attrib['href']
                }

        next_page = 'https://rollersnakes.co.uk' + response.css('a.Pagination__NavItem').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)