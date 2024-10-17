import requests
import sqlite3
from bs4 import BeautifulSoup


# 定义获取天气信息的函数
def get_weather_info(city_id):
    url_template = 'http://www.weather.com.cn/weather/{}.shtml'
    complete_url = url_template.format(city_id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    response = requests.get(complete_url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    forecast_data = []
    days = soup.find('ul', class_='t clearfix').find_all('li')

    for day in days:
        day_date = day.find('h1').get_text(strip=True)
        weather_condition = day.find('p', class_='wea').get_text(strip=True)
        high_temp = day.find('span').get_text(strip=True) if day.find('span') else ''
        low_temp = day.find('i').get_text(strip=True)
        temperature = f"{high_temp}/{low_temp}"
        forecast_data.append((day_date, weather_condition, temperature))

    return forecast_data


# 创建数据库和表格
def initialize_database():
    connection = sqlite3.connect('weather_data.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS forecast (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            forecast_date TEXT,
            condition TEXT,
            temp_range TEXT
        )
    ''')
    connection.commit()
    return connection


# 存储天气信息到数据库
def store_weather_data(location, weather_info, connection):
    cursor = connection.cursor()
    for day_date, condition, temp in weather_info:
        cursor.execute("INSERT INTO forecast (location, forecast_date, condition, temp_range) VALUES (?, ?, ?, ?)",
                       (location, day_date, condition, temp))
    connection.commit()


# 打印数据库中的天气信息
def print_weather_data(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM forecast")
    records = cursor.fetchall()

    print(f"{'ID':<5} {'城市':<10} {'日期':<15} {'天气状况':<20} {'温度范围':<15}")
    for record in records:
        print(f"{record[0]:<5} {record[1]:<10} {record[2]:<15} {record[3]:<20} {record[4]:<15}")


def main():
    # 城市及其对应的代码
    cities = {
        '北京': '101010100',
        '上海': '101020100',
        '福州': '101230101',
        '天津': '101030100'
    }

    # 初始化数据库连接
    db_connection = initialize_database()

    # 获取并存储每个城市的天气信息
    for city_name, city_id in cities.items():
        print(f"获取城市 {city_name} ({city_id}) 的天气信息...")
        weather_info = get_weather_info(city_id)
        store_weather_data(city_name, weather_info, db_connection)

    # 打印数据库中的天气信息
    print_weather_data(db_connection)

    db_connection.close()


if __name__ == '__main__':
    main()


