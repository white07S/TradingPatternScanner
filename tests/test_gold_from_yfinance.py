import yfinance as yf
from tradingpatterns.tradingpatterns import detect_head_shoulder
import datetime as dt


def test_gold_yfinance_long_term():
    ticker = yf.Ticker("GOLD")
    history = ticker.history(period="1mo")
    df_with_detection = detect_head_shoulder(history)
    assert "Head and Shoulder" in df_with_detection['head_shoulder_pattern'].values


def test_tesla_2_hours():

    start_date = dt.datetime.fromisoformat('2023-05-04T02:51:56.734028')
    end_date = dt.datetime.fromisoformat('2023-05-04T04:51:56.734028')

    gold_data = yf.download("TSLA", start=start_date, end=end_date, interval="15m")
    df_with_detection = detect_head_shoulder(gold_data)
    assert "Head and Shoulder" in df_with_detection['head_shoulder_pattern'].values