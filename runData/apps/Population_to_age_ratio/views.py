from django.shortcuts import render
import pandas as pd
import json

def index(request):
    # 載入人口 CSV 檔案，跳過第一行並將第二行設為標題
    df_population = pd.read_csv('data/各縣市人口與年齡之比例.csv', header=1, encoding='utf-8', dtype=str)
    
    # 定義欄位名稱（排除第一個空的識別欄）
    columns = ["年份", "總計", "臺灣地區", "新北市", "臺北市", "桃園市", "臺中市", "臺南市", "高雄市", 
               "宜蘭縣", "新竹縣", "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣", "屏東縣", "臺東縣", 
               "花蓮縣", "澎湖縣", "基隆市", "新竹市", "嘉義市", "金門縣", "連江縣"]

    # 將欄位名稱賦給 DataFrame（排除第一個未命名的欄位）
    df_population.columns = ["Age Group"] + columns

    # 刪除第一個未命名的欄位
    df_population = df_population.drop(columns=["Age Group"])

    # 刪除空的列和欄
    df_population = df_population.dropna(axis=1, how='all').dropna(axis=0, how='all')

    # 去除欄位名稱的任何空白
    df_population.columns = df_population.columns.str.strip()

    # 將字串數字轉換為整數，並將 NaN 值替換為零
    for col in df_population.columns[1:]:
        df_population[col] = df_population[col].str.replace(',', '')
        df_population[col] = df_population[col].fillna(0).astype(int)
    # 按縣市分離資料
    city_data = {}
    cities = columns[1:]  # 縣市名稱列表

    for city in cities:
        city_data[city] = {
            "0-14歲": df_population[["年份", city]].iloc[0:5].set_index("年份").to_dict(orient='list')[city],
            "15-64歲": df_population[["年份", city]].iloc[6:11].set_index("年份").to_dict(orient='list')[city],
            "65歲以上": df_population[["年份", city]].iloc[12:17].set_index("年份").to_dict(orient='list')[city]
        }

    # 從 DataFrame 中提取年份
    years = df_population['年份'].iloc[0:5].tolist()  # 假設年份是前五個條目

    # 計算各年齡層的成長幅度，四捨五入到小數點後兩位
    growth_data = {}
    for city in cities:
        growth_data[city] = {}
        for age_group in ["0-14歲", "15-64歲", "65歲以上"]:
            current_values = city_data[city][age_group]
            growth_values = [0]  # 第一年的成長幅度設為0
            for i in range(1, len(current_values)):
                growth = (current_values[i] - current_values[i-1]) / current_values[i-1] * 100 if current_values[i-1] != 0 else 0
                growth_values.append(round(growth, 2))
            growth_data[city][age_group] = growth_values

    # 將縣市資料轉換為 JSON
    data = json.dumps(city_data)
    growth_data_json = json.dumps(growth_data)

    return render(request, 'PARindex.html', {
        'years': json.dumps(years),
        'data': data,
        'growth_data': growth_data_json
    })
