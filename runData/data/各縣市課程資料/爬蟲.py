import time

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import pandas as pd

# 生成表頭
data = {
    "課程名稱": [],
    "上課地點": [],
    "開放報名": [],
    "開課日期": [],
    "性質": []
}


driver = webdriver.Chrome(service=Service())

# 使 Browser Window 最大化
driver.maximize_window()

driver.get("https://course.taiwanjobs.gov.tw/course/search-history")
time.sleep(3)

#選擇資料之年份
coursesearch_year_dropdown_y = driver.find_element(By.ID, 'coursesearch-time-y')

select = Select(coursesearch_year_dropdown_y)

select.select_by_visible_text('2019')

coursesearch_year_dropdown_m = driver.find_element(By.ID, 'coursesearch-time-m')

select = Select(coursesearch_year_dropdown_m)

select.select_by_visible_text('01')

coursesearch_year_dropdown_year = driver.find_element(By.ID, 'coursesearch-time-year')

select = Select(coursesearch_year_dropdown_year)

select.select_by_visible_text('2022')

coursesearch_year_dropdown_month = driver.find_element(By.ID, 'coursesearch-time-month')

select = Select(coursesearch_year_dropdown_month)

select.select_by_visible_text('12')


#選則縣市:
popup_button = driver.find_element(By.CSS_SELECTOR, '[data-target="#modalPopup"]')  # 替换为实际的按钮 ID
popup_button.click()
time.sleep(2)
checkboxes = driver.find_elements(By.XPATH, '//input[@type="checkbox"]')
# 選擇的縣市
values_to_select = ['15']  

# 选中指定的复选框
for checkbox in checkboxes:
    if checkbox.get_attribute('value') in values_to_select:
        if not checkbox.is_selected():
            checkbox.click()

#關閉複選框
modal_footer = driver.find_element(By.CLASS_NAME, 'modal-footer')

# 在模态框的 footer 元素中找到包含 "確定" 文本的按钮
confirm_button = modal_footer.find_element(By.XPATH, '//button[contains(text(), "確定")]')
confirm_button.click()

time.sleep(3)

#按下選擇
search_button = driver.find_element(By.CSS_SELECTOR, '.btn.btn-blue')
search_button.click()

time.sleep(3)

#選擇頁碼
page = driver.find_element(By.ID, 'page')
select = Select(page)
select.select_by_visible_text(str(1))
i = 1

while page:
    
    if i == 1:
        #抓資料:
        table = driver.find_element(By.CLASS_NAME, 'table-special')


    if i > 1:
        #抓資料:
        table = driver.find_element(By.CLASS_NAME, 'table-responsive')

    # 找到表格中所有行
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # 遍历每一行，并提取每个 <td> 标签中的文本内容
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [cell.text for cell in cells]
        if len(row_data) > 6:
            course_name = row_data[1]
            location = row_data[2]
            registration_date = row_data[3]
            start_date = row_data[4]
            nature = row_data[6]

            data["課程名稱"].append(course_name)
            data["上課地點"].append(location)
            data["開放報名"].append(registration_date)
            data["開課日期"].append(start_date)
            data["性質"].append(nature)
        
    i += 1
    try:
        select.select_by_visible_text(str(i))
    except:
        break
    time.sleep(3)

# 創建DataFrame
df = pd.DataFrame(data)

# 保存到CSV
df.to_csv('高雄市課程資料.csv', index=False, encoding='utf-8-sig')
