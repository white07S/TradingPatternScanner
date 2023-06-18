from scipy.signal import savgol_filter
import numpy as np
import pandas as pd
from pykalman import KalmanFilter
import pywt

'''
Algorithm 1: Basic Head-Shoulder Detection
This algorithm implements a basic detection of the "Head and Shoulder" and "Inverse Head and Shoulder" patterns 
in a data frame. These patterns are significant in financial analysis as they indicate possible market reversals. 
In the code, the algorithm uses a rolling window to track high and low points in the 'High' and 'Low' columns of 
the data frame. It then creates boolean masks to identify where these patterns occur. The identified patterns are 
then added to the data frame in a new 'head_shoulder_pattern' column.
'''

def detect_head_shoulder(df, window=3):
# Define the rolling window
    roll_window = window
    # Create a rolling window for High and Low
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

'''
Algorithm 2: Head-Shoulder Detection with Savitzky-Golay Filter

This algorithm is an improvement of the first one. It first applies the Savitzky-Golay filter to smooth the 'High' and 'Low' columns. 
This filter is used to reduce noise and improve the reliability of pattern detection. 
In addition to the head-shoulder pattern detection of the first algorithm, this algorithm also considers 
the height of the "Head" or "Inverse Head" and introduces a threshold to avoid false pattern 
recognition due to insignificant price changes.
'''
def detect_head_shoulder_filter(df, window=3, threshold=0.01, time_delay=1):
    roll_window = window
    df['High_smooth'] = savgol_filter(df['High'], roll_window, 2) # Apply Savitzky-Golay filter
    df['Low_smooth'] = savgol_filter(df['Low'], roll_window, 2)
    
    df['high_roll_max'] = df['High_smooth'].rolling(window=roll_window).max()
    df['low_roll_min'] = df['Low_smooth'].rolling(window=roll_window).min()
    
    # Define the height of the head and inverse head
    df['head_height'] = df['high_roll_max'] - df['Low'].rolling(window=roll_window).min()
    df['inv_head_height'] = df['High'].rolling(window=roll_window).max() - df['low_roll_min']
    
    # Define the masks for head and shoulder and inverse head and shoulder
    mask_head_shoulder = ((df['head_height'] > threshold) & (df['high_roll_max'] > df['High_smooth'].shift(time_delay)) & (df['high_roll_max'] > df['High_smooth'].shift(-time_delay)) & (df['High_smooth'] < df['High_smooth'].shift(time_delay)) & (df['High_smooth'] < df['High_smooth'].shift(-time_delay)))
    mask_inv_head_shoulder = ((df['inv_head_height'] > threshold) & (df['low_roll_min'] < df['Low_smooth'].shift(time_delay)) & (df['low_roll_min'] < df['Low_smooth'].shift(-time_delay)) & (df['Low_smooth'] > df['Low_smooth'].shift(time_delay)) & (df['Low_smooth'] > df['Low_smooth'].shift(-time_delay)))
    
    df['head_shoulder_pattern'] = np.nan
    df.loc[mask_head_shoulder, 'head_shoulder_pattern'] = 'Head and Shoulder'
    df.loc[mask_inv_head_shoulder, 'head_shoulder_pattern'] = 'Inverse Head and Shoulder'
    
    return df

'''
Algorithm 3: Head-Shoulder Detection with Kalman Filter

In this algorithm, the Kalman Filter is used to smooth the 'High' and 'Low' columns. 
The Kalman Filter is a recursive filter that estimates the state of a system in real time, 
making it more suitable for financial data with its inherent noise and uncertainties. 
This can potentially improve the accuracy of pattern detection. 
The pattern detection process is similar to Algorithm 1, but it operates on the smoothed data.
'''


def kalman_smooth(series, n_iter=10):
    # Initialize Kalman filter
    kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)

    # Use the EM algorithm to estimate the best values for the parameters
    kf = kf.em(series, n_iter=n_iter)

    # Use the observed values of the price to get a rolling mean
    state_means, _ = kf.filter(series.values)

    return state_means.flatten()


def detect_head_shoulder_kf(df, window=3):
    roll_window = window
    df['High_smooth'] = kalman_smooth(df['High'])
    df['Low_smooth'] = kalman_smooth(df['Low'])
    
    df['high_roll_max'] = df['High_smooth'].rolling(window=roll_window).max()
    df['low_roll_min'] = df['Low_smooth'].rolling(window=roll_window).min()
    
    mask_head_shoulder = ((df['high_roll_max'] > df['High_smooth'].shift(1)) & (df['high_roll_max'] > df['High_smooth'].shift(-1)) & (df['High_smooth'] < df['High_smooth'].shift(1)) & (df['High_smooth'] < df['High_smooth'].shift(-1)))
    mask_inv_head_shoulder = ((df['low_roll_min'] < df['Low_smooth'].shift(1)) & (df['low_roll_min'] < df['Low_smooth'].shift(-1)) & (df['Low_smooth'] > df['Low_smooth'].shift(1)) & (df['Low_smooth'] > df['Low_smooth'].shift(-1)))
    
    df['head_shoulder_pattern'] = np.nan
    df.loc[mask_head_shoulder, 'head_shoulder_pattern'] = 'Head and Shoulder'
    df.loc[mask_inv_head_shoulder, 'head_shoulder_pattern'] = 'Inverse Head and Shoulder'
    
    return df

'''
Algorithm 4: Head-Shoulder Detection with Wavelet Denoising

In this algorithm, wavelet denoising is applied to the 'High' and 'Low' columns before 
the pattern detection process. Wavelet denoising is an effective technique for eliminating 
noise while preserving the key features in the data. This can make the pattern detection process 
more robust and reliable, especially in the presence of high frequency noise in the data. 
Similar to the previous algorithms, the head-shoulder pattern detection is performed on the denoised data.
'''

def wavelet_denoise(series, wavelet='db1', level=1):
    # Perform wavelet decomposition
    coeff = pywt.wavedec(series, wavelet, mode="per")
    # Set detail coefficients for levels > level to zero
    for i in range(1, len(coeff)):
        coeff[i] = pywt.threshold(coeff[i], value=np.std(coeff[i])/2, mode="soft")
    # Perform inverse wavelet transform
    return pywt.waverec(coeff, wavelet, mode="per")


def detect_head_shoulder_wavelet(df, window=3):
    roll_window = window
    df['High_smooth'] = wavelet_denoise(df['High'], 'db1', level=1)
    df['Low_smooth'] = wavelet_denoise(df['Low'], 'db1', level=1)
    
    df['high_roll_max'] = df['High_smooth'].rolling(window=roll_window).max()
    df['low_roll_min'] = df['Low_smooth'].rolling(window=roll_window).min()
    
    mask_head_shoulder = ((df['high_roll_max'] > df['High_smooth'].shift(1)) & (df['high_roll_max'] > df['High_smooth'].shift(-1)) & (df['High_smooth'] < df['High_smooth'].shift(1)) & (df['High_smooth'] < df['High_smooth'].shift(-1)))
    mask_inv_head_shoulder = ((df['low_roll_min'] < df['Low_smooth'].shift(1)) & (df['low_roll_min'] < df['Low_smooth'].shift(-1)) & (df['Low_smooth'] > df['Low_smooth'].shift(1)) & (df['Low_smooth'] > df['Low_smooth'].shift(-1)))
    
    df['head_shoulder_pattern'] = np.nan
    df.loc[mask_head_shoulder, 'head_shoulder_pattern'] = 'Head and Shoulder'
    df.loc[mask_inv_head_shoulder, 'head_shoulder_pattern'] = 'Inverse Head and Shoulder'
    
    return df
