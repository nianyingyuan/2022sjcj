import requests
from bs4 import BeautifulSoup
import sqlite3

# 目标网页URL
url = 'https://www.shanghairanking.cn/rankings/bcur/2021'  # 请替换为实际的URL

# 使用 requests 获取网页内容
response = requests.get(url)
content = response.content

# 解析网页内容
soup = BeautifulSoup(content, 'html.parser')

# 找到包含大学排名信息的表格
ranking_table = soup.find('table', class_='rk-table')

# 创建或连接到SQLite数据库
database = sqlite3.connect('schools_rank.db')
db_cursor = database.cursor()

# 创建数据表，如果表不存在
db_cursor.execute('''CREATE TABLE IF NOT EXISTS university_ranking
                      (rank TEXT, school_name TEXT, province_city TEXT, school_type TEXT, total_score TEXT)''')

# 遍历表格中的每一行，获取数据
for entry in ranking_table.find_all('tr')[1:]:  # 跳过表头
    columns = entry.find_all('td')
    rank_value = columns[0].get_text(strip=True)
    university_name = columns[1].get_text(strip=True)
    location = columns[2].get_text(strip=True)
    type_of_school = columns[3].get_text(strip=True)
    score = columns[4].get_text(strip=True)

    # 插入数据到数据库中
    db_cursor.execute('''INSERT INTO university_ranking (rank, school_name, province_city, school_type, total_score)
                         VALUES (?, ?, ?, ?, ?)''', (rank_value, university_name, location, type_of_school, score))

# 提交数据到数据库
database.commit()

# 查询并打印数据库中的所有记录
db_cursor.execute("SELECT * FROM university_ranking")
records = db_cursor.fetchall()
for record in records:
    # 清除记录中的换行符
    cleaned_record = [field.replace('\n', '') for field in record]

    # 打印处理后的记录
    print(tuple(cleaned_record))

# 关闭数据库连接
database.close()

print("大学排名数据已成功保存至数据库")
