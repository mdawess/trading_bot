import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from yahoo_fin import stock_info as si
from time import sleep
import alpaca_trade_api as tradeapi

# Imports the technical indicators from helper file
from money_helper import Technicals

#API_KEY = 'PKJHZE9C0O6SSUC3I3LR'
#API_SECRET = 'Iapyj1gABGOEyFuyqgraK6kQpbRABIFfD7pU5OJX'
#APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

## Establishes connection to alpaca API
#api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')
#account = api.get_account()
##print(api.list_positions())
#print(account.status)

# Message to print if program is run outside of market hours
MESSAGE = """The market is closed.
Please try again between 9:30 and 16:30 EST."""

# Restriction if account is under $25,000 for pattern day trading 
TRADE_LIMIT = 3
ACCOUNT_THRESHOLD = 25000

# Current amount, updated at EOD
ACCOUNT_AMOUNT = 50000

STOCKS = ['AAPL', 'ABBV', 'AMGN', 'AZN', 'BABA', 'BAC', 'BMY', 'CHL', 'CMCSA', 
          'COST', 'CRM', 'CSCO', 'DIS', 'FB', 'HD', 'INTC', 'JNJ', 'JPM',
          'KO', 'LLY', 'MA', 'MCD', 'MRK', 'MSFT', 'NKE', 'NVS', 'ORCL', 'PEP', 
          'PFE', 'PG', 'PYPL', 'SAP', 'T', 'TM', 'TMO', 'TSM', 'UNH', 'V', 'VZ',
          'WMT', 'XOM', 'UNH', 'PM', 'IBM', 'AMD', 'WFC', 'CVS', 'MMM', 'SBUX',
          'QCOM', 'MO', 'CAT', 'DHR', 'AMT', 'LIN', 'GILD', 'C', 'HON', 'FIS', 
          'RTX', 'VRTX', 'MDLZ', 'CI', 'BDX', 'UPS', 'PLD', 'LOW', 'DUK', 'TJX',
          'ATVI', 'AXP', 'ICE', 'MU', 'CSX', 'GE', 'MS', 'WM', 'EMR', 'EBAY', 
          'WBA', 'GM', 'FDX', 'ROK', 'KHC', 'BYND', 'TSN', 'K', 'TRV', 'BBI', 
          'USO']

one = ['AAPL', 'ABBV', 'AMGN', 'AZN', 'BABA', 'BAC', 'BMY', 'CHL', 'CMCSA']

def initialize():
    """Establishes the necessary DataFrame based on either the list of pre
    selected stocks or based on user input. Pre-established list gives better
    results due to larger amount of data.
    """
    
    TICKERS = one
    #TICKERS = []
    #for i in range(int(input('How many tickers do you want to analyze? '))):
        #ticker = str(input('What ticker(s) would you like to trade? '))
        #TICKERS.append(ticker)
        
    DATA_FILE = []
    for ticker in TICKERS:
        stock = yf.Ticker(ticker)
        data = stock.history('1y')
        DATA_FILE.append(data) 
        
    return TICKERS, DATA_FILE

def market_hours():
    """Defines the timespan in which the market is open.
    """
    
    market_open = False
    time = datetime.now()
    
    if (time.hour,time.minute) >= (9,30) and (time.hour,time.minute) <= (16,30):
        market_open = True
        
    else:
        print(MESSAGE)
        
    return market_open

#============================ Checking Indicators ==============================

#Make inputs lowercase in final build
def check_ma(TICKERS, DATA_FILE, USER_CHOICE):
    """Pulls the moving average data from the technical indicators class.
    """
    #Add a differentiator between buy signals 
    
    technicals = Technicals(TICKERS, DATA_FILE)
    buy = False
    
    if technicals.ma_50(USER_CHOICE) > technicals.ma_200(USER_CHOICE):
        buy = True
    
    elif technicals.ma_50(USER_CHOICE) > technicals.ma_100(USER_CHOICE):   
        buy = True
        
    return buy
    
def check_volume(TICKERS, DATA_FILE, USER_CHOICE):
    """Pulls the volume data from the pre-defined data frame using the 
    volume class.
    """
    
    technicals = Technicals(TICKERS, DATA_FILE)
    volume = technicals.volume(USER_CHOICE)
    
    buy = False
    if int(volume[-1]) >= int(volume[-2]) * 100:
        buy = True
    
    return buy #volume

def check_rsi(TICKERS, DATA_FILE, USER_CHOICE):
    """Checks the most recent RSI and returns buy or sell signal based on
    value.
    """
    technicals = Technicals(TICKERS, DATA_FILE)
    rsi = technicals.rsi(TICKERS, DATA_FILE, USER_CHOICE)
    
    # Make this make sense, decide on a return variable to indicate what to do
    buy = False
    sell = False
    if rsi[-1] >= 30:
        buy = True
    elif rsi[-1] >= 70:
        sell = True
        
    return buy #rsi

def get_signals(TICKERS, DATA_FILE):
    """Get the data from the three signal checkers for each individual 
    ticker and append each to their respective list. List is in order that
    the tickers were specified.
    """
    
    ma_signals = []
    volumes = []
    rsi_list = []
    
    for USER_CHOICE in TICKERS:
        ma_signal = check_ma(TICKERS, DATA_FILE, USER_CHOICE)
        ma_signals.append(ma_signal)
        volume = check_volume(TICKERS, DATA_FILE, USER_CHOICE)
        volumes.append(volume)
        rsi = check_rsi(TICKERS, DATA_FILE, USER_CHOICE)
        rsi_list.append(rsi)
        
    return ma_signals, volumes, rsi_list

#===============================================================================

def get_current_price(TICKERS, DATA_FILE):
    """Returns the a dictionary with the ticker as the key and a list of 
    values containing the current price and the previous day close.
    """
    
    current_prices = {}
    
    # Has the current price and price of previous close for comparison
    for ticker in TICKERS:
        current_prices[ticker] = [si.get_live_price(ticker), 
                                  DATA_FILE[TICKERS.index(ticker)]['Close'][-1]]
    
    return current_prices
    
def make_dictionary(TICKERS, ma_signals, volumes, rsi_list):
    """Returns a dictionary containing the three signals for each of the 
    user selected tickers.
    """
    
    best_buy = {}
    for i in range(len(TICKERS)):
        best_buy[TICKERS[i]] = ma_signals[i], volumes[i], rsi_list[i]
        
    return best_buy

# API already has this feature, may need for future (QT)
def portfolio():
    """Manages the makeup of the portfolio by not allowing any one asset to 
    make up over x% of the portfolio.
    """
    # total portfolio value = ACCOUNT_AMOUNT
    # Update at EOD each day
    # Check the buy order list and calculate the current price as a % of total 
    #  account value, and potentially stop purchase of same share (somehow)
    pass

# API already has this feature, may need for future (QT)  
def create_price_log():
    """Return the ticker symbol, purchase price, sale price and time of both
    transactions as a dictionary.
    """
    
    # 'AAPL': (300, time, 315, time)
    day_trade = 0
    price_log = {}
    for i in price_log:
        pass
    # if key[1] == key[-1]:
    # day_trade += 1
    # if day trade == 3 then signal program to stop
    
def stocks_to_buy(TICKERS, ticker_to_signal):
    """Executes the buy order for a given stock when is meets the criteria.
    """
    buys = {}
    for key in ticker_to_signal:
        for i in range(3):
            count = 0
            ma = False
            if ticker_to_signal[key][i] == True:
                count += 1
            elif ticker_to_signal[key][1] == True:
                ma = True
        # Dictates how many of the technicals need to signal buy
        if count >= 1 or ma == True:
            buys[key] = ['Buy', si.get_live_price(key), datetime.now()]
    if len(buys) == 0:
        print('No tickers met the criteria')
        return buys
    else:
        return buys
    
def get_sell_order(buy_order):
    """Check current holdings to see if stop loss/profit is met.
    """
    sell = False
    sell_order = {}
    
    for ticker in buy_order:
        t = datetime.now()
        p = si.get_live_price(ticker)
        if p >= buy_order[ticker][1] * 1.05:
            sell = True
            buy_order[ticker] = []
            sell_order[ticker] = [p, t]
        elif p <= buy_order[ticker][1] * 0.98:
            sell = True
            buy_order[ticker] = []
            sell_order[ticker] = [p, t]
                
    return sell_order#, buy_order
     
def main():
    """Collects data and executes trades."""
    # Gets the initial user input 
    tickers, data_file = initialize()
    
    # Record the amount purchased 
    total_cost = 0
    # Quantity of shares to be purchased
    quantity = '10'
    if total_cost < ACCOUNT_AMOUNT:
        while total_cost < ACCOUNT_AMOUNT:
        
            ma_signals, volumes, rsi_list = get_signals(tickers, data_file)
            
            # Signals in order ma, volume, rsi
            ticker_to_signal = make_dictionary(tickers, ma_signals, volumes, rsi_list)
            # Generates a dictionary with stocks to buy based on technical signals 
            buy_order = stocks_to_buy(tickers, ticker_to_signal)
            
            # Takes the stocks in buy_order and purchases them
            for stock in buy_order:
                api.submit_order(
                    symbol=stock,
                    side='buy',
                    type='market',
                    qty=quantity,
                    time_in_force='day',
                    order_class='bracket',
                    take_profit=dict(
                        limit_price=(str(si.get_live_price(stock) *1.1)),
                    ),
                    stop_loss=dict(
                        stop_price=(str(si.get_live_price(stock) * 0.95)),
                        limit_price=(str(si.get_live_price(stock) * 0.93)),
                    )
                )
                # Tracks the total amount spent to compare to total portfolio value
                total_cost += float(si.get_live_price(stock)*int(quantity))
                print('Purchase successful!')
                print(total_cost)
                """Allow the bot to take profit properly."""
            # Takes the stocks that meet the take_profit/stop_loss and sells   
            sell_order = get_sell_order(buy_order)
            if len(sell_order) > 0:
                for stonk in sell_order:
                    api.submit_order(
                        symbol=stonk,
                        side='sell',
                        type='market',
                        qty=quantity,
                        time_in_force='day',
                        order_class='bracket',
                        take_profit=dict(
                            limit_price=(str(si.get_live_price(stock) *1.02)),
                        ),
                        stop_loss=dict(
                            stop_price=(str(si.get_live_price(stock) * 0.93)),
                            limit_price=(str(si.get_live_price(stock) * 0.95)),
                        )
                    )        
                    # Reduces the total cost by amount sold
                    total_cost -= float(si.get_live_price(stock)*int(quantity))
                    print('Sale successful!')
    elif total_cost >= ACCOUNT_AMOUNT:
        while total_cost >= ACCOUNT_AMOUNT:
            sell_order = get_sell_order(buy_order)
            for stonk in sell_order:
                api.submit_order(
                    symbol=stonk,
                    side='sell',
                    type='market',
                    qty=quantity,
                    time_in_force='day',
                    order_class='bracket',
                    take_profit=dict(
                        limit_price=(str(si.get_live_price(stock) *1.02)),
                    ),
                    stop_loss=dict(
                        stop_price=(str(si.get_live_price(stock) * 0.93)),
                        limit_price=(str(si.get_live_price(stock) * 0.95)),
                    )
                )        
                # Reduces the total cost by amount sold
                total_cost -= float(si.get_live_price(stock)*int(quantity))
                print('Sale successful!')        
            sleep(15)
    #main()
        
while market_hours() == True:
    #main()
    pass
