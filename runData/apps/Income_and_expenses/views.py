from django.shortcuts import render
import pandas as pd
import numpy as np
import json

def index(request):
    df_expenditure = pd.read_csv('data/各縣市家庭經常性支出.csv', header=1, encoding='utf-8', dtype=str)
    df_revenue = pd.read_csv('data/各縣市家庭經常性收入.csv', header=1, encoding='utf-8', dtype=str)

    columns = ["年份", "總計", "臺灣地區", "新北市", "臺北市", "桃園市", "臺中市", "臺南市", "高雄市", 
               "宜蘭縣", "新竹縣", "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣", "屏東縣", "臺東縣", 
               "花蓮縣", "澎湖縣", "基隆市", "新竹市", "嘉義市", "金門縣", "連江縣"]

    df_expenditure.columns = columns
    df_revenue.columns = columns

    df_expenditure = df_expenditure.dropna(axis=1, how='all').dropna(axis=0, how='all')
    df_revenue = df_revenue.dropna(axis=1, how='all').dropna(axis=0, how='all')

    df_expenditure.columns = df_expenditure.columns.str.strip()
    df_revenue.columns = df_revenue.columns.str.strip()

    df_expenditure['年份'] = df_expenditure['年份'].astype(str)
    df_revenue['年份'] = df_revenue['年份'].astype(str)

    for col in df_expenditure.columns[1:]:
        df_expenditure[col] = df_expenditure[col].str.replace(',', '').astype(int)
        df_revenue[col] = df_revenue[col].str.replace(',', '').astype(int)

    growth_rates = {}
    avg_diff = {}
    for col in df_expenditure.columns[1:]:
        expenditure_y = df_expenditure[col].values
        revenue_y = df_revenue[col].values
        x = np.arange(len(expenditure_y))

        # 進行線性回歸並且算出斜率
        slope, intercept = np.polyfit(x, revenue_y - expenditure_y, 1)
        initial_value = expenditure_y[0]
        if initial_value != 0:
            growth_rate = (slope / initial_value) * 100  # 轉成百分比
        else:
            growth_rate = 0
        growth_rates[col] = round(growth_rate, 2)  # 四捨五入

        avg_diff[col] = round(np.mean(revenue_y - expenditure_y), 2)

    years = json.dumps(df_expenditure['年份'].tolist())
    data_expenditure = {col: df_expenditure[col].tolist() for col in df_expenditure.columns[1:]}
    data_revenue = {col: df_revenue[col].tolist() for col in df_revenue.columns[1:]}

    data = {
        'expenditure': data_expenditure,
        'revenue': data_revenue
    }
    data_json = json.dumps(data)
    growth_rates_json = json.dumps(growth_rates)
    avg_diff_json = json.dumps(avg_diff)

    return render(request, 'IAEindex.html', {
        'years': years,
        'data': data_json,
        'growth_rates': growth_rates_json,
        'avg_diff': avg_diff_json
    })
