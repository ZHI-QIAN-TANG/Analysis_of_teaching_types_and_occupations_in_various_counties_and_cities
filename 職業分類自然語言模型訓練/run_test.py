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

# 測試用
course_name = "GA + Power BI大數據行銷分析實作班"
predicted_category = predict_course_category(course_name)
print(f"課程名稱: {course_name}")
print(f"預測職業分類: {predicted_category}")
