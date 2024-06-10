from django.shortcuts import render
import pandas as pd
import numpy as np
import json

def index(request):
    df = pd.read_csv('data/新生兒人數.csv', header=None, skiprows=2, encoding='utf-8', dtype=str)

    df.columns = ["年份", "總計", "臺灣地區", "新北市", "臺北市", "桃園市", "臺中市", "臺南市", "高雄市", 
                  "宜蘭縣", "新竹縣", "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣", "屏東縣", "臺東縣", 
                  "花蓮縣", "澎湖縣", "基隆市", "新竹市", "嘉義市", "金門縣", "連江縣"]

    df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')
    df.columns = df.columns.str.strip()
    df['年份'] = df['年份'].astype(str)

    for col in df.columns[1:]:
        df[col] = df[col].str.replace(',', '').astype(int)

    years = json.dumps(df['年份'].tolist())
    data = {col: df[col].tolist() for col in df.columns[1:]}
    data_json = json.dumps(data)

    growth_rates = {}
    for col in df.columns[1:]:
        y = df[col].values
        x = np.arange(len(y))
        # 進行線性回歸並且算出斜率
        slope, intercept = np.polyfit(x, y, 1)
        initial_value = y[0]
        if initial_value != 0:
            growth_rate = (slope / initial_value) * 100  # 轉成百分比
        else:
            growth_rate = 0
        growth_rates[col] = round(growth_rate, 2)  # 四捨五入
    growth_rates_json = json.dumps(growth_rates)

    return render(request, 'NONindex.html', {'years': years, 'data': data_json, 'growth_rates': growth_rates_json})
