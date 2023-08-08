import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import mplfinance as mpf

def load_data_from_file(filename):
    data = pd.read_csv(filename, header=None, names=["timestamp", "open", "high", "low", "close", "volume", "closetime", "quoteassetvolume", "trades", "takerbuybaseassetvolume", "takerbuyquoteassetvolume", "ignore"])
    data["timestamp"] = pd.to_datetime(data["timestamp"], unit='ms')
    data.set_index("timestamp", inplace=True)
    return data

def plot_candlestick_last_12_months(data):
    last_12_months_data = data.loc[data.index >= (data.index[-1] - pd.DateOffset(months=12))]
    mpf.plot(last_12_months_data, type='candle', style='binance', title='Bitcoin Trading History (Last 12 Months)', ylabel='Price')


def plot_candlestick(data):
    mpf.plot(data, type='candle', style='binance', title='Bitcoin Trading History', ylabel='Price')

if __name__ == "__main__":
    file_name = 'BTCUSDT_trading_history.txt'

    data = load_data_from_file(file_name)
    if data is not None:
        plot_candlestick_last_12_months(data)
    else:
        print(f"Failed to load data from {file_name}. Make sure the file exists and is correctly formatted.")
