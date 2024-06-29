import json
from pycoingecko import CoinGeckoAPI
import configparser

def check_coin_name(crypto_name):
    cg = CoinGeckoAPI()
    all_coins_list = cg.get_coins_list()
    symbols = [coin["symbol"] for coin in all_coins_list]

    if crypto_name.lower() in [symbol.lower() for symbol in symbols]:
        print(f"Coin '{crypto_name}' found!")
        return True
    else:
        print(f"Coin '{crypto_name}' not found.")
        return False

def update_config(coin_name, mode, time):
    config = configparser.ConfigParser()
    config.read('example.cfg')

    if not check_coin_name(coin_name):
        print("Coin not found, cannot update configuration.")
        return

    if mode not in [0, 1, 'line', 'candle']:
        print("Invalid mode. Must be either 0 (candle), 1 (line), 'line', or 'candle'.")
        return

    if mode in [0, 'candle']:
        mode_str = 'candle'
    else:
        mode_str = 'line'

    if not isinstance(time, (int, float)) or time <= 0:
        print("Time must be a positive number.")
        return

    if time.is_integer():
        time_str = str(int(time))
    else:
        time_str = "{:.1f}".format(time)

    config.set('base', 'currency', coin_name.upper())
    config.set('base', 'efresh_interval_minutes', time_str)

    for screen in config.sections():
        if screen!= 'base':
            config.set(screen, 'ode', mode_str)

    with open('configuration.cfg', 'w') as configfile:
        config.write(configfile)
    print("Updated configuration written to configuration.cfg")

# Get user input with default values
input_name = input("Input coin name (btc): ").strip()
if not input_name:
    input_name = 'btc'

input_mode = input("Input mode 0 = candle, 1 = line: ").strip()
if not input_mode:
    input_mode = 0
else:
    if input_mode.lower() == 'line':
        input_mode = 1
    elif input_mode.lower() == 'candle':
        input_mode = 0
    else:
        input_mode = int(input_mode)

input_time = input("Input time (in minutes): ").strip()
if not input_time:
    input_time = 15.0
else:
    input_time = float(input_time)

update_config(input_name, input_mode, input_time)
