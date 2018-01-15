import scrapy


class CurrencyAttributeGetter(scrapy.Spider):
    name = 'currency_attribute_getter'

    def start_requests(self):
        with open('currency_names.txt', 'r') as f:
            for line in f:
                line = line.strip()
                yield scrapy.Request(u'https://coinmarketcap.com' + line + '#markets',
                                     self.parse)

    def parse(self, response):
        required_pair_list = [
            'XRP',
            'BTC',
            'USD',
            'ETH',
            'USDT',
        ]
        title = response.url[37:response.url.find("#")]
        output_string = ''
        out_put_file = open("currency_data.txt", "a+")
        output_string = title
        markets = response.css('tr')
        for market in markets:
            if market.css('td').extract():
                source = market.css('td')[1].css('a::text')[0].extract()
                pair = market.css('td')[2].css('a::text')[0].extract().split('/')
                volume = market.css('td')[3].css('span::text')[0].extract().strip()
                # volume_percentage = response.css('tr')[1].css('td::text')[5].extract().strip() # Not using Currently
                price = market.css('td')[4].css('span::text')[0].extract().strip()
                updated = market.css('td::text')[6].extract().strip()
                if updated == 'Recently' and (pair[0] in required_pair_list or pair[1] in required_pair_list):
                    output_string += (
                        ',' +
                        source
                        + '|' +
                        pair[0]+':'+pair[1]
                        + '|' +
                        price
                        + '|' +
                        volume
                    )
        output_string += '\n'
        out_put_file.write(output_string)
        out_put_file.close()


