class TradeOption:
    def __init__(self, currency, profit_margin, bank_1, bank_2):
        self.profit_margin = profit_margin
        self.bank_1 = bank_1
        self.bank_2 = bank_2
        self.currency = currency

    def __repr__(self):
        return repr((self.currency, self.profit_margin, self.bank_1, self.bank_2))


class DataManipulator:
    def __init__(self):
        trade_options = self.load_all_data()
        self.show_best_trade_option(trade_options)

    def load_all_data(self):
        all_trade_options = []
        with open('data/currency_data.txt', 'r') as file:
            for line in file:
                # Load all data into one array
                all_data = line.strip().split('^')
                # If only one bank data ignore currency
                if len(all_data)-1 < 1:
                    continue
                else:
                    valid = self.return_best_trade_option_for_one_currency(all_data)
                    if valid:
                        all_trade_options.append(valid)
        return all_trade_options

    def show_best_trade_option(self, all_trade_options):
        all_trade_options = sorted(all_trade_options, key=lambda option: option.profit_margin, reverse=True)
        for i in range(len(all_trade_options)):
            print(all_trade_options[i])

    def return_best_trade_option_for_one_currency(self, data):
        maximum_price_bank = None
        minimum_price_bank = None
        maximum_price_bank_price = 0.0
        minimum_price_bank_price = 0.0
        profit_margin = None
        currency = data[0]
        for bank in data[1:]:
            bank_data = bank.strip().split('|')
            if not maximum_price_bank:
                maximum_price_bank = bank
            if not minimum_price_bank:
                minimum_price_bank = bank
            if maximum_price_bank and minimum_price_bank:
                maximum_price_bank_price = float(maximum_price_bank.split('|')[2].replace('$', '').replace(',', ''))
                minimum_price_bank_price = float(minimum_price_bank.split('|')[2].replace('$', '').replace(',', ''))
                current_bank_price = float(bank_data[2].replace('$', '').replace(',', ''))
                if current_bank_price > maximum_price_bank_price:
                    maximum_price_bank = bank
                elif minimum_price_bank_price < current_bank_price:
                    minimum_price_bank = bank

        profit_margin = float(maximum_price_bank_price - minimum_price_bank_price)
        if profit_margin != 0.0:
            return TradeOption(currency, profit_margin, maximum_price_bank, minimum_price_bank)
        return None

    def sorter(self, all_trade_options):
        for i in range(len(all_trade_options)):
            for j in range(len(all_trade_options)-i):
                if all_trade_options[j].profit_margin > all_trade_options[i].profit_margin:
                    temp = all_trade_options[j]
                    all_trade_options[j] = all_trade_options[i]
                    all_trade_options[i] = temp
        return all_trade_options