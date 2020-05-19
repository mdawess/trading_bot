import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
from yahoo_fin import stock_info as si
from time import sleep
from money_helper import Technicals


MESSAGE = """The market is closed.
Please try again between 9:30 and 16:30 EST."""
TRADE_LIMIT = 3
ACCOUNT_THRESHOLD = 25000
ACCOUNT_AMOUNT = 1000

STOCKS = ['AAPL', 'ABBV', 'AMGN', 'AZN', 'BABA', 'BAC', 'BMY', 'CHL', 'CMCSA', 
          'COST', 'CRM', 'CSCO', 'DIS', 'FB', 'HD', 'INTC', 'JNJ', 'JPM',
          'KO', 'LLY', 'MA', 'MCD', 'MRK', 'MSFT', 'NKE', 'NVS', 'ORCL', 'PEP', 
          'PFE', 'PG', 'PYPL', 'SAP', 'T', 'TM', 'TMO', 'TSM', 'UNH', 'V', 'VZ',
          'WMT', 'XOM', 'UNH', 'PM', 'IBM', 'AMD', 'WFC', 'CVS', 'MMM', 'SBUX',
          'QCOM', 'MO', 'CAT', 'DHR', 'AMT', 'LIN', 'GILD', 'C', 'HON', 'FIS', 
          'RTX', 'VRTX', 'MDLZ', 'CI', 'BDX', 'UPS', 'PLD', 'TGT', 'DUK', 'TJX',
          'ATVI', 'AXP', 'ICE', 'MU', 'CSX', 'GE', 'MS', 'WM', 'EMR', 'EBAY', 
          'WBA', 'GM', 'FDX', 'ROK', 'KHC', 'BYND', 'TSN', 'K', 'TRV', 'BBI', 
          'USO']

def initialize():
    """Create the necessary initial variables based on user input"""
    # Allow user to enter a comma seperated set of tickers 
    TICKERS = STOCKS
    #TICKERS = []
    #for i in range(int(input('How many tickers do you want to analyze? '))):
        #ticker = str(input('What ticker(s) would you like to trade? '))
        #TICKERS.append(ticker)
        
    DATA_FILE = []
    for ticker in TICKERS:
        stock = yf.Ticker(ticker)
        data = stock.history('1y')
        DATA_FILE.append(data) 
        
    # CHange user choice to be a list of tickers so not everything has to change = TICKERS
    #USER_CHOICE = str(input('Which stock would you like to analyze first? '))
    return TICKERS, DATA_FILE#, USER_CHOICE

def market_hours():
    """Defines the timespan in which the market is open"""
    
    market_open = False
    time = datetime.now()
    
    if (time.hour,time.minute) >= (9,30) and (time.hour,time.minute) <= (16,30):
        market_open = True
        
    else:
        print(MESSAGE)
        
    return market_open

#============================ Checking Indicators ==============================

""" Make inputs lowercase in final build """
def check_ma(TICKERS, DATA_FILE, USER_CHOICE):
    """Compare Moving averages """
    #Add a differentiator between buy signals 
    
    technicals = Technicals(TICKERS, DATA_FILE)
    buy = False
    
    if technicals.ma_50(USER_CHOICE) > technicals.ma_200(USER_CHOICE):
        buy = True
    
    elif technicals.ma_50(USER_CHOICE) > technicals.ma_100(USER_CHOICE):   
        buy = True
        
    return buy
    
def check_volume(TICKERS, DATA_FILE, USER_CHOICE):
    """Check for volume spikes."""
    
    technicals = Technicals(TICKERS, DATA_FILE)
    volume = technicals.volume(USER_CHOICE)
    
    buy = False
    if int(volume[-1]) >= int(volume[-2]) * 100:
        buy = True
    
    return buy #volume

def check_rsi(TICKERS, DATA_FILE, USER_CHOICE):
    """CHecks the most recent RSI and returns buy or sell signal based on
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
    """Get the data from the three signal checkers."""
    
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
    """Returns the current_prices for the selected TICKERS"""
    
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

def sell(ticker, buy_price):
    """Generates the buy and sell criteria for the stock that was purchased 
    and stores it in a dictionary.
    """
    sell = False
    current_price = si.get_live_price(ticker)
    if current_price == buy_price * 1.05:
        #sell the stock
        sell = True
    elif current_price == buy_price* 0.98:
        #sell the stock 
        sell = True 
        
    return sell
    

def portfolio():
    """Manages the makeup of the portfolio by not allowing any one asset to 
    make up over x% of the portfolio.
    """
    # total portfolio value = ACCOUNT_AMOUNT
    # Update at EOD each day
    # Check the buy order list and calculate the current price as a % of total 
    #     account value, and potentially stop purchase of same share (somehow) 
def create_price_log():
    """Return the ticker symbol, purchase price, sale price and time of both
    transactions as a dictionary."""
    
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
        if count >= 1 or ma == True:
            buys[key] = 'Buy', si.get_live_price(key), datetime.now()
    if len(buys) == 0:
        return 'No tickers met the criteria'
    else:
        return buys
    
def execute_buy(buy_order):
    """Connects to broker and executes the desired trade based on stocks_to_buy
    criteria."""
    
    pass

def get_sell_order(buy_order):
    """Check current holdings to see if stop loss/profit is met."""
    sell = False
    sell_order = {}
    for ticker in buy_order:
        if si.get_live_price(ticker) >= buy_order[ticker][1] * 1.05:
            sell = True
            buy_order[ticker] = ''
            sell_order[ticker] = si.get_live_price(ticker), datetime.now()
        elif si.get_live_price(ticker) <= buy_order[ticker][1] * 0.98:
            sell = True
            buy_order[ticker] = ''
            sell_order[ticker] = si.get_live_price(ticker), datetime.now()
            
    return sell, buy_order, sell_order   

# Make this a seperate function to return the buy order      
def main():
    
    # Gets the initial user input 
    tickers, data_file = initialize()
    
    # Refreshes the data every t seconds
    t = 10
    i = 0
    #while i < 1:
    ma_signals, volumes, rsi_list = get_signals(tickers, data_file)
    
    # Signals in order ma, volume, rsi
    ticker_to_signal = make_dictionary(tickers, ma_signals, volumes, rsi_list)
    buy_order = stocks_to_buy(tickers, ticker_to_signal)
    print(buy_order)
    sell_order = get_sell_order(buy_order)
    print(sell_order)
        
        #sleep(t)
        

#while market_hours() == True:
main()

# Make a dictionary to record the buy price, sell price and time of the trade
# Limit trades buy only allowing buy and sell to execute 3 times
# buy = 0, sell = 0 and increment them each time a buy or sell is made