import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import wandb

# 初始化 W&B
wandb.init(project="Run_occupation_classification")

# 讀取CSV文件
df = pd.read_csv('data.csv')

# 過濾資料
df = df[df['職業分類'] != '其他']

# 需要的列
df = df[['課程名稱', '職業分類']]

# 在資料中分出訓練集與測試集
train_texts, val_texts, train_labels, val_labels = train_test_split(df['課程名稱'].tolist(), df['職業分類'].tolist(), test_size=0.2)

# 使用BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

# 將標籤轉為ID
label2id = {label: idx for idx, label in enumerate(set(train_labels))}

# 保存標籤到ID的建立關係
with open("label2id.txt", "w") as f:
    for label, idx in label2id.items():
        f.write(f"{label}\t{idx}\n")

def tokenize(texts):
    return tokenizer(texts, padding=True, truncation=True, return_tensors='pt')

train_encodings = tokenize(train_texts)
val_encodings = tokenize(val_texts)

# 創建數據對象
class TextDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
        self.label2id = {label: idx for idx, label in enumerate(set(labels))}
        self.id2label = {idx: label for label, idx in self.label2id.items()}
        self.numeric_labels = [self.label2id[label] for label in labels]

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.numeric_labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = TextDataset(train_encodings, train_labels)
val_dataset = TextDataset(val_encodings, val_labels)

# 加載預訓練的BERT模型
model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=len(train_dataset.label2id))

# 定義訓練參數
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy="epoch",
    report_to="wandb" 
)

# 創建Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# 訓練模型
trainer.train()

# 保存模型
model.save_pretrained('./model')
tokenizer.save_pretrained('./model')

# 加載模型和tokenizer
model = BertForSequenceClassification.from_pretrained('./model')
tokenizer = BertTokenizer.from_pretrained('./model')

def predict_course_category(course_name):
    inputs = tokenizer(course_name, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()
    return train_dataset.id2label[prediction]

# 測試用
course_name = "中餐美食料理班"
predicted_category = predict_course_category(course_name)
print(f"課程名稱: {course_name}")
print(f"預測職業分類: {predicted_category}")
