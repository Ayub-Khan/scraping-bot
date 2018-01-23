from nose.tools import set_trace
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
        with open('currency_data.txt', 'r') as file:
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
            if all_trade_options[i].profit_margin>7.0:
                print('Arbitrage % :' + str(round(all_trade_options[i].profit_margin, 2)) +
                      'Currency : ' +
                      str(all_trade_options[i].currency) + ' buy from ' +
                      all_trade_options[i].bank_2 +
                      ' sell on ' + all_trade_options[i].bank_1)

    def return_best_trade_option_for_one_currency(self, data):
        different_pairs = {}
        results = []
        currency = data[0]
        markets = data[1:]
        for i in range(len(markets)):
            bank_data = markets[i].strip().split('|')
            pair_value = bank_data[1]
            count = 0
            for j in range(len(markets)):
                j_pair_values = markets[j].strip().split('|')[1].split(':')
                i_pair_values = pair_value.split(':')
                if i_pair_values[0]==j_pair_values[0] and i_pair_values[1]==j_pair_values[1]:
                    count += 1

            if count > 1:
                try:
                    different_pairs[pair_value].append(markets[i])
                except KeyError:
                    different_pairs[pair_value] = [markets[i]]

        if not different_pairs:
            return

        for pair in different_pairs.keys():
            data = different_pairs[pair]
            maximum_price_bank = None
            minimum_price_bank = None
            maximum_price_bank_price = 0.0
            minimum_price_bank_price = 0.0
            profit_margin = None
            for bank in data:
                bank_data = bank.strip().split('|')
                if not maximum_price_bank:
                    maximum_price_bank = bank
                    minimum_price_bank = bank
                elif maximum_price_bank and minimum_price_bank:
                    maximum_price_bank_price = float(maximum_price_bank.split('|')[2].replace('$', '').replace(',', ''))
                    minimum_price_bank_price = float(minimum_price_bank.split('|')[2].replace('$', '').replace(',', ''))
                    current_bank_price = float(bank_data[2].replace('$', '').replace(',', ''))
                    if current_bank_price > maximum_price_bank_price:
                        maximum_price_bank = bank
                    elif minimum_price_bank_price > current_bank_price:
                        minimum_price_bank = bank

            maximum_price_bank_price = float(maximum_price_bank.split('|')[2].replace('$', '').replace(',', ''))
            minimum_price_bank_price = float(minimum_price_bank.split('|')[2].replace('$', '').replace(',', ''))
            profit_margin = (float(maximum_price_bank_price - minimum_price_bank_price)*100)/minimum_price_bank_price
            if profit_margin != 0.0:
                results.append(TradeOption(currency, profit_margin, maximum_price_bank, minimum_price_bank))

        if not results:
            return

        if len(results)==1:
            return results[0]
        try:
            return sorted(results, key=lambda result: result.profit_margin, reverse=True)[0]
        except Exception as e:
            print currency
            print different_pairs
            print results
            print e

    def sorter(self, all_trade_options):
        for i in range(len(all_trade_options)):
            for j in range(len(all_trade_options)-i):
                if all_trade_options[j].profit_margin > all_trade_options[i].profit_margin:
                    temp = all_trade_options[j]
                    all_trade_options[j] = all_trade_options[i]
                    all_trade_options[i] = temp
        return all_trade_options
