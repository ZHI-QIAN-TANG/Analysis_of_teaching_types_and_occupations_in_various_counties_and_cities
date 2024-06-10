from django.shortcuts import render
import os
import pandas as pd
import json

def index(request):
    # 定義 Excel 文件所在的資料夾
    excel_directory = 'data/各縣市職業組成比例'
    
    # 讀取所有 Excel 文件並處理數據
    city_data = {}

    for root, _, files in os.walk(excel_directory):
        for file in files:
            if file.endswith('.xlsx'):
                file_path = os.path.join(root, file)
                city_name = os.path.splitext(file)[0]  # 提取城市名稱
                df = pd.read_excel(file_path, index_col=0)  # 假設第一列是索引
                df.insert(0, '縣市', city_name)  # 將縣市名稱插入到第一列
                city_data[city_name] = df.to_dict(orient='records')  # 將 DataFrame 轉換為字典
    # 將 city_data 轉換為 JSON 字串
    city_data_json = json.dumps(city_data, ensure_ascii=False)

    context = {
        "city_data_json": city_data_json,
        "cities": list(city_data.keys())  # 城市名稱列表
    }
    return render(request, 'ORindex.html', context)