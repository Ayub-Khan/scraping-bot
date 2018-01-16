with open('currency_data.txt', 'r') as all_currency_file:
    out_put_file = open("currency_names.txt", "a+")
    for line in all_currency_file:
        if len(line) > 60:
            out_put_file.write('/currencies/' + line.split('^')[0].strip() + '/\n')
    out_put_file.close()

