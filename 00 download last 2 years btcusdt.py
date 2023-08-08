'''
Module: A collection of a few scripts for BTC-USDT basic stats

Author: Łukasz Zmywaczyk <l.zmywaczyk@gmail.com>

Description: First execute "00 download last 2 years btcusdt.py" in order to download history data, used by other scripts.
'''
import requests
import json
from datetime import datetime, timedelta

def get_binance_data(symbol, interval, start_time, end_time):
    base_url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': int(start_time.timestamp() * 1000),
        'endTime': int(end_time.timestamp() * 1000),
        'limit': 1000,  # Maximum allowed by Binance API
        
    }
    response = requests.get(base_url, params=params)
    return response.json()

def save_to_txt(filename, data):
    with open(filename, 'w') as f:
        for candlestick in data:
            f.write(','.join(str(item) for item in candlestick) + '\n')

if __name__ == "__main__":
    symbol = 'BTCUSDT'  # Trading pair for Bitcoin (BTC) and USDT (Tether)
    interval = '1d'     # Daily interval (1 day)

    # Calculate start and end times for the last 2 years
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=365*2)

    data = get_binance_data(symbol, interval, start_time, end_time)
    if data:
        file_name = f"{symbol}_trading_history.txt"
        save_to_txt(file_name, data)
        print(f"Data for {symbol} saved to {file_name}.")
    else:
        print(f"Failed to retrieve data for {symbol}. Check your API settings.")
