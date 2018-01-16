import os
from data_manipulator import DataManipulator

def main():
    print("Crypto Currency Trade Suggestion Bot")
    print("*Starting Pulling Data*")
    os.remove('currency_data.txt')
    os.system('scrapy runspider currency_attribute_getter.py')
    print("Data has been Updated")
    print('Best Trade Options')
    DataManipulator()

if __name__ == "__main__":
    main()
    raw_input()