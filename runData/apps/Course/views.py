from django.shortcuts import render
import os
import pandas as pd
import json

def index(request):
    # 定義 CSV 檔案所在的資料夾
    csv_directory = 'data/各縣市課程資料'
    
    # 讀取並合併所有 CSV 檔案
    combined_data = read_and_combine_csv(csv_directory)

    city_data = {}
    cities = list(combined_data.keys())

    for city, df in combined_data.items():
        total_count = df.shape[0]
        category_counts = df['職業分類'].value_counts().to_dict()
        city_data[city] = {
            "total_count": total_count,
            "category_counts": category_counts
        }

    # 將 city_data 轉換為 JSON 字串
    city_data_json = json.dumps(city_data, ensure_ascii=False)

    context = {
        "city_data_json": city_data_json,
        "cities": cities
    }
    return render(request, 'Cindex.html', context)

def read_and_combine_csv(directory):
    combined_data = {}
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                city_name = os.path.splitext(file)[0]  # 使用檔案名稱作為城市名稱
                df = pd.read_csv(file_path)
                combined_data[city_name] = df
    
    return combined_data
