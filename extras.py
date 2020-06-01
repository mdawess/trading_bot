#Extra stuff for testing/ extra functions

#tests
one = ['AAPL', 'ABBV', 'AMGN', 'AZN', 'BABA', 'BAC', 'BMY', 'CHL', 'CMCSA']
two = ['COST', 'CRM', 'CSCO', 'DIS', 'FB', 'HD', 'INTC', 'JNJ', 'JPM']
three = ['KO', 'LLY', 'MA', 'MCD', 'MRK', 'MSFT', 'NKE', 'NVS', 'ORCL', 'PEP']
four = ['PFE', 'PG', 'PYPL', 'SAP', 'T', 'TM', 'TMO', 'TSM', 'UNH', 'V', 'VZ']
five = ['WMT', 'XOM', 'UNH', 'PM', 'IBM', 'AMD', 'WFC', 'CVS', 'MMM', 'SBUX']
six = ['QCOM', 'MO', 'CAT', 'DHR', 'AMT', 'LIN', 'GILD', 'C', 'HON', 'FIS']
seven = ['RTX', 'VRTX', 'MDLZ', 'CI', 'BDX', 'UPS', 'PLD', 'LOW', 'DUK', 'TJX']
eight = ['ATVI', 'AXP', 'ICE', 'MU', 'CSX', 'GE', 'MS', 'WM', 'EMR', 'EBAY']
nine = ['WBA', 'GM', 'FDX', 'ROK', 'KHC', 'BYND', 'TSN', 'K', 'TRV', 'BBI', 'USO']

# API essentials 

#api = tradeapi.REST('<key_id>', '<secret_key>', api_version='v2') # or use ENV Vars shown below
#account = api.get_account()
#api.list_positions()


#account = api.get_account()
#account.status
##=> 'ACTIVE'

#api.submit_order(
    #symbol='SPY',
    #side='buy',
    #type='market',
    #qty='100',
    #time_in_force='day',
    #order_class='bracket',
    #take_profit=dict(
        #limit_price='305.0',
    #),
    #stop_loss=dict(
        #stop_price='295.5',
        #limit_price='295.5',
    #)
#)

# Backup main() function

#def main():
    
    ## Gets the initial user input 
    #tickers, data_file = initialize()
    
    ## Refreshes the data every t seconds
    #t = 10
    #i = 0
    ##while i < 1:
    #ma_signals, volumes, rsi_list = get_signals(tickers, data_file)
    
    ## Signals in order ma, volume, rsi
    #ticker_to_signal = make_dictionary(tickers, ma_signals, volumes, rsi_list)
    #buy_order = stocks_to_buy(tickers, ticker_to_signal)
    #print(buy_order)
    #sell_order = get_sell_order(buy_order)
    #print(sell_order)
        
        ##sleep(t)
        
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