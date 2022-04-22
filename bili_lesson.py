import pandas as pd
import requests
import json
import datetime as dt

def get_binance_bars(symbol, interval, startTime, endTime):
    url = "https://api.binance.com/api/v3/klines"
    start_time = str(int(startTime.timestamp()*1000))
    end_time = str(int(startTime.timestamp()*1000))
    limit = "1000"
    req_params = {
        "symbol":symbol,
        "interval":interval,
        "startTime":start_time,
        "endTime":end_time,
        "limit":limit
    }

    df = pd.DataFrame(json.loads(requests.get(url, params= req_params).text))

    if len(df.index) == 0:
        return None

    df.open = df.open.astype("float")
    df.close = df.close.astype("float")
    df.high = df.high.astype("float")
    df.low = df.low.astype("float")
    df.volumn = df.volumn.astype("float")
    df.index = [dt.datetime.fromtimestamp(x/100.0) for x in df.datetime]
    return df

def get_data():
    df_list = []
    last_datetime = dt.datetime(2020,1,1)
    while True:
        new_df = get_binance_bars("BTCUSDT","1d",last_datetime,dt.datetime.now())
        if new_df is None:
            break
        df_list.append(new_df)
        last_datetime = max(new_df.index) + df.timedelta(0,1)
    
    df = pd.concat(df_list)
    return df

df = get_data()