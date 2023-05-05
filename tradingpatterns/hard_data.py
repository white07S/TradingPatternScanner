import pandas as pd, random
def draw_around(center, amplitude):
    date_rng = pd.date_range(start='1/1/2020', periods=len(center), freq='D')
    data = {'date': date_rng}

    semi_amplitude = amplitude / 2
    data['High'] = [cent + semi_amplitude for cent in center]
    data['Low'] = [cent - semi_amplitude for cent in center]
    data['Open'] = [dalow + random.random() * amplitude for dalow in data['Low']]
    data['Close'] = [dahigh - random.random() * amplitude for dahigh in data['High']]
    data['Volume'] = [random.randint(1000, 10000) for _ in range(len(center))]
    return data

def draw_around_fn(filename, amplitude):
    #Thanks, ChatGPT 4 for the models
    data = pd.read_csv(filename, parse_dates=True)

    semi_amplitude = amplitude / 2
    data['High'] = [cent + semi_amplitude for cent in data['Price']]
    data['Low'] = [cent - semi_amplitude for cent in data['Price']]
    data['Open'] = [dalow + random.random() * amplitude for dalow in data['Low']]
    data['Close'] = [dahigh - random.random() * amplitude for dahigh in data['High']]
    data['Volume'] = [random.randint(1000, 10000) for _ in range(len(data['Price']))]
    return data

def draw_around_fn_close(filename, amplitude):
    #Thanks, ChatGPT 4 for the models
    data = pd.read_csv(filename, parse_dates=True)

    semi_amplitude = amplitude / 2
    data['High'] = [cent + semi_amplitude for cent in data['Price']]
    data['Low'] = [cent - semi_amplitude for cent in data['Price']]
    data['Open'] = [dalow + random.random() * amplitude for dalow in data['Low']]
    data['Close'] = data['Price']
    data['Volume'] = [random.randint(1000, 10000) for _ in range(len(data['Price']))]
    return data

def generate_sample_df_with_pattern(pattern):
    date_rng = pd.date_range(start='1/1/2020', end='1/10/2020', freq='D')
    data = {'date': date_rng}
    if pattern == 'Head and Shoulder':
        data['Open'] = [90, 85, 80, 90, 90 , 75, 75, 80, 85, 90]
        data['High'] = [95, 90, 85, 95, 100, 85, 80, 85, 90, 95]
        data['Low'] = [80, 75, 70, 80, 85 , 70, 65, 70, 75, 80]
        data['Close'] = [85, 85, 80, 90, 85 , 80, 75, 80, 85, 90]
        data['Volume'] = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    elif pattern == 'Inverse Head and Shoulder':
        data['Open'] = [20, 25, 30, 20, 25, 30, 35, 30, 25, 20]
        data['High'] = [25, 30, 35, 25, 30, 35, 40, 35, 30, 25]
        data['Low'] = [15, 20, 25, 15, 20, 25, 30, 25, 20, 15]
        data['Close'] = [20, 25, 30, 20, 25, 30, 35, 30, 25, 20]
        data['Volume'] = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    elif pattern == "Double Top":
        return draw_around_fn('double_top.csv', 1)
    elif pattern == "Double Bottom":
        return draw_around_fn('double_bottom.csv', 1)
    elif pattern == "Triple Top":
        return draw_around_fn_close('triple_top.csv', 1)
    elif pattern == "Triple Bottom":
        return draw_around_fn_close('triple_bottom.csv', 1)
    elif pattern == "Ascending Triangle":
        return draw_around_fn_close('ascending_triangle.csv', 1)
    elif pattern == "Descending Triangle":
        return draw_around_fn_close('descending_triangle.csv', 1)
    df = pd.DataFrame(data)
    return df