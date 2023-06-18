import pandas as pd
def generate_sample_df_with_pattern(pattern):
    date_rng = pd.date_range(start='1/1/2020', end='1/10/2020', freq='D')
    data = {'date': date_rng}
    if pattern == 'Head and Shoulder':
        data['Open'] = [90, 85, 80, 90, 85, 80, 75, 80, 85, 90]
        data['High'] = [95, 90, 85, 95, 90, 85, 80, 85, 90, 95]
        data['Low'] = [80, 75, 70, 80, 75, 70, 65, 70, 75, 80]
        data['Close'] = [90, 85, 80, 90, 85, 80, 75, 80, 85, 90]
        data['Volume'] = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    elif pattern == 'Inverse Head and Shoulder':
        data['Open'] = [20, 25, 30, 20, 25, 30, 35, 30, 25, 20]
        data['High'] = [25, 30, 35, 25, 30, 35, 40, 35, 30, 25]
        data['Low'] = [15, 20, 25, 15, 20, 25, 30, 25, 20, 15]
        data['Close'] = [20, 25, 30, 20, 25, 30, 35, 30, 25, 20]
        data['Volume'] = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    elif pattern == "Double Top" or "Double Bottom" or "Ascending Triangle" or "Descending Triangle":
        data['High'] = [95, 90, 85, 95, 90, 85, 80, 85, 90, 95]
        data['Low'] = [80, 75, 70, 80, 75, 70, 65, 70, 75, 80]
        df = pd.DataFrame(data)
        df.iloc[3:5,1] =100
        df.iloc[6:8,1] =70
        df.iloc[6:9,2] =70
    df = pd.DataFrame(data)
    return df


import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Function to generate random OHLCV data
def generate_random_data(length):
    close_values = np.random.randint(100, 200, length).tolist()
    return {
        'Open': [value - random.randint(0, 10) for value in close_values],
        'High': [value + random.randint(0, 10) for value in close_values],
        'Low': [value - random.randint(0, 10) for value in close_values],
        'Close': close_values,
        'Volume': np.random.randint(1000, 2000, length).tolist(),
    }

# Function to inject head and shoulders and inverse head and shoulders patterns
def inject_patterns(data):
    shoulder_height = random.randint(120, 140)
    head_height = random.randint(150, 170)
    inv_shoulder_depth = random.randint(60, 80)
    inv_head_depth = random.randint(40, 60)
    
    # Left Shoulder
    data['High'][3] = shoulder_height
    data['Close'][3] = shoulder_height - random.randint(0, 5)
    
    # Head
    data['High'][5] = head_height
    data['Close'][5] = head_height - random.randint(0, 5)
    
    # Right Shoulder
    data['High'][7] = shoulder_height
    data['Close'][7] = shoulder_height - random.randint(0, 5)
    
    # Left Inverse Shoulder
    data['Low'][13] = inv_shoulder_depth
    data['Close'][13] = inv_shoulder_depth + random.randint(0, 5)
    
    # Inverse Head
    data['Low'][15] = inv_head_depth
    data['Close'][15] = inv_head_depth + random.randint(0, 5)
    
    # Right Inverse Shoulder
    data['Low'][17] = inv_shoulder_depth
    data['Close'][17] = inv_shoulder_depth + random.randint(0, 5)
    
    return data

def generate_data_head_shoulder(n):
    # Start date
    start_date = datetime.now()

    # Dataframe for storing data
    df = pd.DataFrame()

    # Generate n Head and Shoulders patterns
    for i in range(n):
        data = generate_random_data(20)  # 20 data points are needed for one full pattern
        data = inject_patterns(data)
        
        temp_df = pd.DataFrame(data)
        temp_df['Datetime'] = pd.date_range(start=start_date, periods=20, freq='D')  # Adjust the frequency accordingly
        start_date += timedelta(days=20)  # Adjust the timedelta accordingly
        
        df = df.append(temp_df, ignore_index=True)

    df = df[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]

    return df
