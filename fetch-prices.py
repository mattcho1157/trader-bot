import os
import pandas as pd

from dotenv import load_dotenv
from binance.client import Client

SYMBOLS= ['ETHUSDT']
TIMEFRAMES = ['5m', '15m', '30m', '1h', '2h', '4h']

# load environment variables
load_dotenv()
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

print('connecting to binance client...')
client = Client(api_key, api_secret)

def fetch_prices(symbol, timeframe):
    print(f'fetching {symbol}-{timeframe} prices...')
    earliest_time = client._get_earliest_valid_timestamp(symbol, timeframe)
    candles = client.get_historical_klines(symbol, timeframe, earliest_time)

    df = pd.DataFrame(candles).iloc[:, :6]
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    df.set_index('time', inplace=True)
    df.index = pd.to_datetime(df.index, unit='ms')
    df.to_csv(f'prices/{symbol}-{timeframe}.csv')

for symbol in SYMBOLS:
    for timeframe in TIMEFRAMES:
        fetch_prices(symbol, timeframe)