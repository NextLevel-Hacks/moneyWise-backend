
from time import sleep
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import  MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import datetime


from dotenv import load_dotenv
import os

load_dotenv()


SEC_KEY = os.getenv("ALPACA_KEY")
PUB_KEY = os.getenv("ALPACA_SECRET")

list_universe = [
    'AAPL',   # Apple Inc.
    'MSFT',   # Microsoft Corporation
    'AMZN',   # Amazon.com, Inc.
]

# client = StockHistoricalDataClient(api_key=PUB_KEY, secret_key=SEC_KEY, url_override="https://paper-api.alpaca.markets/v2")

# intraday_request_params = StockBarsRequest(
#     symbol_or_symbols=list_universe,
#     timeframe = TimeFrame(1, TimeFrameUnit.Day),
#     start = "2024-01-01 00:00:00",
#     adjustment='all'
# )

# # retrieve dataframe of stock data
# intraday_bars = client.get_stock_bars(intraday_request_params).df
# intraday_bars.reset_index(inplace=True)



# Instantiate the trading client
api = TradingClient(PUB_KEY, SEC_KEY, raw_data=True, paper=False)

def wait_for_order_completion(api, order_id, timeout=120):
    start_time = datetime.now()
    while (datetime.now() - start_time).seconds < timeout:
        order_status = api.get_order_by_id(order_id)
        if order_status['status'] in ['filled', 'canceled', 'expired', 'rejected']:
            return order_status
        sleep(2)  # Check every 2 seconds
    return None  # Timeout

def trade_share(symbol, usd_amount):

    print(f"Executing BUY for {usd_amount} USD of {symbol}")
    order = api.submit_order(MarketOrderRequest(symbol=symbol, notional = usd_amount, side=OrderSide.BUY, time_in_force=TimeInForce.DAY))
    order_status = wait_for_order_completion(api, order['id'])
    if order_status and order_status['status'] == 'filled':
        print(f"Order {order['id']} filled successfully.")


trade_share("NFLX",1000)