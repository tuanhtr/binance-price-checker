
import requests
import json
from datetime import datetime
import time
from sql import SQL
from datetime import timedelta
import math

SYMBOL_KEY = "symbol"
PRICE_KEY = "price"

TIME_STAMP = 3602 # seconds
COMPARE_VALUE = 2.5 # Change percent
QUERY_STAMP = 2

uncheck_list = ["SCBTC", "HOTBTC", "NCASHBTC", "NPXSBTC", "DENTBTC", "STORMBTC", "KEYBTC"]


coin_info = dict()


class BinancePrice:

    @classmethod
    def execute(cls):
        try:
            alt_coins_info = cls._get_binance_info()
            price_changed = []
            print("EXECUTE {0}".format(str(datetime.now())))
            # Loop in all result
            for alt_coin in alt_coins_info:
                try:
                    if "BTC" not in alt_coin[SYMBOL_KEY] or alt_coin[SYMBOL_KEY] in uncheck_list:
                        continue

                    # Get price change information,
                    change_info = cls._get_price_change_info(alt_coin, TIME_STAMP)

                    # Compare changed percent with COMPARE_VALUE
                    if change_info.change_percent >= COMPARE_VALUE:
                        price_changed.append(change_info)

                except Exception:
                    continue
                    # print(ex)
                    # print("Something wrong!!! {0}".format(alt_coin))

            # print(price_changed)
            if len(price_changed) > 0:
                for coin in price_changed:
                    print("Name: {0} - Current time: {1} - Current price: {2} - Percent: {3} ".format(coin.alt_coin_name, str(datetime.now()), coin.current_price, coin.change_percent))
                print("=================================================================")
            return price_changed

        except Exception as ex:
            print(ex)

    @classmethod
    def _get_binance_info(cls):
        url = "https://www.binance.com/api/v1/ticker/allPrices"
        response = requests.get(url)
        return response.json()

    @classmethod
    def _get_price_change_info(cls, alt_coin_info, step_time):
        current_time = datetime.now()
        # select_time = current_time - timedelta(seconds=step_time)
        alt_coin = alt_coin_info[SYMBOL_KEY]
        current_price = alt_coin_info[PRICE_KEY]

        # Add coin value to database
        # id = SQL.save_coin(alt_coin, current_price, current_time)
        # id = id - step_time
        # if id < 0:
        #     id = 0

        # Add coin value to dict
        if alt_coin not in coin_info:
            coin_info[alt_coin] = []
        else:
            if len(coin_info[alt_coin]) > (TIME_STAMP/QUERY_STAMP):
                del coin_info[alt_coin][0]
        coin_info[alt_coin].append(current_price)

        # Get value from database and compare
        # prv_coin_value = SQL.get_coin_price(alt_coin, select_time)

        # Get value from list
        prv_coin_value = coin_info[alt_coin][0]

        current_price = float(current_price)
        prv_coin_value = float(prv_coin_value)

        if float(current_price) < float(prv_coin_value):
            percent = (current_price - prv_coin_value)*100 / current_price
        else:
            percent = (current_price - prv_coin_value)*100 / prv_coin_value
        return ChangeInfo(alt_coin, current_price, percent, current_time)


class ChangeInfo:

    def __init__(self, alt_coin_name, current_price, percent, current_time):
        self.alt_coin_name = alt_coin_name
        self.current_price = current_price
        self.change_percent = percent
        self.current_time = current_time


if __name__ == "__main__":

    coin_info = {}
    while True:
        BinancePrice.execute()
        time.sleep(QUERY_STAMP)
