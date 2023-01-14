import pandas as pd
import numpy as np

class Patterns:
    def __init__(self,df,rolling_window):
        self.df = df
        self.rolling_window = rolling_window
    def detect_head_shoulder(self,df, window=3):
    # Define the rolling window
        roll_window = window

        # Create a rolling window for high and low
        df['high_roll_max'] = df['High'].rolling(window=roll_window).max()
        df['low_roll_min'] = df['Low'].rolling(window=roll_window).min()

        # Create a boolean mask for Head and Shoulder pattern
        mask_head_shoulder = ((df['high_roll_max'] > df['High'].shift(1)) & (df['high_roll_max'] > df['High'].shift(-1)) & (df['High'] < df['High'].shift(1)) & (df['High'] < df['High'].shift(-1)))
        # Create a boolean mask for Inverse Head and Shoulder pattern
        mask_inv_head_shoulder = ((df['low_roll_min'] < df['Low'].shift(1)) & (df['low_roll_min'] < df['Low'].shift(-1)) & (df['Low'] > df['Low'].shift(1)) & (df['Low'] > df['Low'].shift(-1)))

        # Create a new column for Head and Shoulder and its inverse pattern and populate it using the boolean masks
        df['head_shoulder_pattern'] = np.nan
        df.loc[mask_head_shoulder, 'head_shoulder_pattern'] = 'Head and Shoulder'
        df.loc[mask_inv_head_shoulder, 'head_shoulder_pattern'] = 'Inverse Head and Shoulder'

        return df
    
    def detect_multiple_tops_bottoms(self,df, window=3):
    # Define the rolling window
        roll_window = window

        # Create a rolling window for high and low
        df['high_roll_max'] = df['High'].rolling(window=roll_window).max()
        df['low_roll_min'] = df['Low'].rolling(window=roll_window).min()
        df['close_roll_max'] = df['Close'].rolling(window=roll_window).max()
        df['close_roll_min'] = df['Close'].rolling(window=roll_window).min()

        # Create a boolean mask for multiple top pattern
        mask_top = (df['high_roll_max'] >= df['High'].shift(1)) & (df['close_roll_max'] < df['Close'].shift(1))
        # Create a boolean mask for multiple bottom pattern
        mask_bottom = (df['low_roll_min'] <= df['Low'].shift(1)) & (df['close_roll_min'] > df['Close'].shift(1))

        # Create a new column for multiple top bottom pattern and populate it using the boolean masks
        df['multiple_top_bottom_pattern'] = np.nan
        df.loc[mask_top, 'multiple_top_bottom_pattern'] = 'Multiple Top'
        df.loc[mask_bottom, 'multiple_top_bottom_pattern'] = 'Multiple Bottom'

        return df
    
    def calculate_support_resistance(self, df, window=3):
    # Define the rolling window
        roll_window = window
        # Set the number of standard deviation
        std_dev = 2

        # Create a rolling window for high and low
        df['high_roll_max'] = df['high'].rolling(window=roll_window).max()
        df['low_roll_min'] = df['low'].rolling(window=roll_window).min()

        # Calculate the mean and standard deviation for high and low
        mean_high = df['high'].rolling(window=roll_window).mean()
        std_high = df['high'].rolling(window=roll_window).std()
        mean_low = df['low'].rolling(window=roll_window).mean()
        std_low = df['low'].rolling(window=roll_window).std()

        # Create a new column for support and resistance
        df['support'] = mean_low - std_dev * std_low
        df['resistance'] = mean_high + std_dev * std_high
        return df

    def detect_triangle_pattern(self,df, window=3):
        # Define the rolling window
        roll_window = window

        # Create a rolling window for high and low
        df['high_roll_max'] = df['High'].rolling(window=roll_window).max()
        df['low_roll_min'] = df['Low'].rolling(window=roll_window).min()

        # Create a boolean mask for ascending triangle pattern
        mask_asc = (df['high_roll_max'] >= df['High'].shift(1)) & (df['low_roll_min'] <= df['Low'].shift(1)) & (df['Close'] > df['Close'].shift(1))
        # Create a boolean mask for descending triangle pattern
        mask_desc = (df['high_roll_max'] <= df['High'].shift(1)) & (df['low_roll_min'] >= df['Low'].shift(1)) & (df['Close'] < df['Close'].shift(1))

        # Create a new column for triangle pattern and populate it using the boolean masks
        df['triangle_pattern'] = np.nan
        df.loc[mask_asc, 'triangle_pattern'] = 'Ascending Triangle'
        df.loc[mask_desc, 'triangle_pattern'] = 'Descending Triangle'

        return df