import os
import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# 加載模型和預測
model = BertForSequenceClassification.from_pretrained('./model')
tokenizer = BertTokenizer.from_pretrained('./model')

# 加載標籤
label2id = {}
with open("label2id.txt", "r") as f:
    for line in f:
        label, idx = line.strip().split("\t")
        label2id[label] = int(idx)

# 定義預測函數
def predict_course_category(course_name):
    inputs = tokenizer(course_name, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()
    predicted_label = [label for label, idx in label2id.items() if idx == prediction][0]
    return predicted_label

# 指定CSV文件所在的資料夾
folder_path = '各縣市課程資料'

# 獲取資料夾檔名
file_names = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# 對每個文件進行處理
for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    
    # 加载CSV文件
    df = pd.read_csv(file_path)
    
    # 預測職業分類並將結果填加到CSV文件中
    predicted_categories = []
    for course_name in df['課程名稱']:
        predicted_category = predict_course_category(course_name)
        predicted_categories.append(predicted_category)
        print("課程名稱 = " ,course_name)
        print("職業分類 = ", predicted_category)
    
    df['職業分類'] = predicted_categories
    
    # 保存文件
    df.to_csv(file_path, index=False)
