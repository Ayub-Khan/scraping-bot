import scrapy

class CurrencyGetter(scrapy.Spider):
    name = "curency_getter"
    start_urls = [
        'https://coinmarketcap.com/all/views/all/',
    ]

    def parse(self, response):
        currencies = response.css('a.currency-name-container::attr(href)').extract()
        with open('currency_names.txt', 'wb') as f:
            for currency in currencies:
                f.write(currency+'\n')
