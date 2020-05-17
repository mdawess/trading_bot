import numpy as np
import pandas as pd

# For when I figure out how to add options 
class Greeks:
    
    def __init__(self):
        pass
    
    def delta(self):
        """Rate of change of option value per $1 change in underlying stock
        price.(Velocity)"""
        pass
    
    def gamma(self):
        """Rate of change of delta.(acceleration)"""
        pass
    
    def vega(self):
        """Measures implied volatility. How much option prices should change 
        in correspondance with a one point change in implied volatility."""
        pass
    
    def theta(self):
        """Amount option loses in value per day when out of the money.
        Time decay"""
        pass
    
    def rho(self):
        """Change in option price corresponding to changes in interest rates."""
        pass
        
class Technicals:
    
    def __init__(self, tickers, data_file):
        """Main technical indicators used for predicting stock movements.
        Includes 50, 100, 200 day moving averages, RSI, MACD, OBV"""
        
        self.watchlist = tickers
        self.datafile = data_file
        
    def ma_50(self, user_choice):
        """calculate the 50 day moving average"""
        sigma = np.array(self.datafile[self.watchlist.index(user_choice)]['Close'])

        moving_average = sigma[:50].sum() / 50
        return moving_average
    
    def ma_100(self, user_choice):
        """calculate the 100 day moving average"""
        sigma = np.array(self.datafile[self.watchlist.index(user_choice)]['Close'])

        moving_average = sigma[:100].sum() / 100
        
        return moving_average
    
    def ma_200(self, user_choice):
        """calculate the 200 day moving average"""
        sigma = np.array(self.datafile[self.watchlist.index(user_choice)]['Close'])

        moving_average = sigma[:200].sum() / 200
        return moving_average
    
    def rsi(self, tickers, data_file, user_choice):
        """From https://stackoverflow.com/questions/20526414
        /relative-strength-index-in-python-pandas"""
        
        window_length = 14
        
        close = self.datafile[self.watchlist.index(user_choice)]['Close']
        # Get the difference in price from previous step
        delta = close.diff()
        # Get rid of the first row, which is NaN since it did not have a previous 
        # row to calculate the differences
        delta = delta[1:] 
        
        # Make the positive gains (up) and negative gains (down) Series
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        
        # Calculate the EWMA
        roll_up1 = up.ewm(span=window_length).mean()
        roll_down1 = down.abs().ewm(span=window_length).mean()
        
        # Calculate the RSI based on EWMA
        RS1 = roll_up1 / roll_down1
        RSI = 100.0 - (100.0 / (1.0 + RS1))      
        
        return RSI
    
    def volume(self, user_choice):
        """Retrieve the volume from the data frame"""
        
        vol = np.array(self.datafile[self.watchlist.index(user_choice)]['Close'])
    
        return vol
        