from django.shortcuts import render
import os
import pandas as pd
import json

def index(request):
    # 定義 CSV 檔案所在的資料夾
    csv_directory = 'data/各縣市補習班名單'
    
    # 讀取並合併所有 CSV 檔案
    combined_df = read_and_combine_csv(csv_directory)

    # 按縣市進行分組並統計補習班總數和各類別數量
    cities = combined_df['地區縣市'].unique()
    city_data = {}

    for city in cities:
        city_df = combined_df[combined_df['地區縣市'] == city]
        total_count = city_df.shape[0]
        category_counts = city_df['短期補習班類別'].value_counts().to_dict()
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
    return render(request, 'CSindex.html', context)

def read_and_combine_csv(directory):
    combined_df = pd.DataFrame()
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    return combined_df
