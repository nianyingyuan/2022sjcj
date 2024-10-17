import requests
from bs4 import BeautifulSoup
import re

# 指定要爬取的网址
url = 'http://www.shanghairanking.cn/rankings/bcur/2020'

# 发送GET请求获取网页内容
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 设置正确的编码
    response.encoding = response.apparent_encoding

    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到大学排名信息
    table = soup.find('table')

    # 打印表头
    header = f"{'排名':<10} {'学校名称':<30} {'省市':<15} {'学校类型':<15} {'总分':<10}"
    print(header)
    print('-' * len(header))  # 打印分隔线

    # 遍历表格行获取数据
    for row in table.find_all('tr')[1:]:  # 跳过表头
        cols = row.find_all('td')
        if len(cols) >= 5:  # 确保有足够的列
            rank = cols[0].text.strip()  # 获取排名

            # 获取学校名称并去除多余信息
            university = cols[1].text.strip()
            university_cleaned = re.sub(r'\s*（.*?）', '', university)  # 去除括号及其内容
            university_cleaned = university_cleaned.split()[0]  # 取第一个部分

            province_city = cols[2].text.strip()  # 获取省市
            school_type = cols[3].text.strip()  # 获取学校类型
            total_score = cols[4].text.strip()  # 获取总分

            # 打印每一行数据
            row_output = f"{rank:<10} | {university_cleaned:<30} | {province_city:<15} | {school_type:<15} | {total_score:<10}"
            print(row_output)
            print('-' * len(row_output))  # 打印分隔线
else:
    print(f'请求失败，状态码: {response.status_code}')
