1.runData: 用於將資料圖像化
(開啟方式: Django的開啟方式一樣)
(使用python manage.py runserver)

2.資料/各縣市課程資料:
有個叫做web_crawler的py檔案用於抓資料
(直接啟動就好)

3.職業分類自然語言模型訓練: 運於NLP將課程名稱分類出課程類別
	1.先跑run_train
	2.在跑run_test看看資料對不對
	3.最後跑Run_occupation_classification開始整理資料