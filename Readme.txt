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

4.每個資料夾都有Required_libraries，這是拿來整理出用了那些函式庫的

5.報告網址: https://www.canva.com/design/DAGH0-vcOZ4/UJhib0o_8lQ6dngv4J3Ufg/edit?utm_content=DAGH0-vcOZ4&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
