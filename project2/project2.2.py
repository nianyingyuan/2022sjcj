import requests
import re
import sqlite3


def fetch_html(page_num, query_parameters):
    base_url = ("http://66.push2.eastmoney.com/api/qt/clist/get?"
                "cb=jQuery112409097606620255823_1696662149317&pn=1&pz=20&po=1&np=" + str(page_num) +
                "&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&" + query_parameters +
                "&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1696662149318")

    response = requests.get(base_url)
    regex_pattern = "\"diff\":\\[(.*?)\\]"
    extracted_data = re.findall(regex_pattern, response.text, re.S)
    return extracted_data


def process_stock_data(query_params, page_num):
    # Retrieve the JSON data from the API
    json_data = fetch_html(page_num, query_params)
    stocks_data = json_data[0].split("},")

    # Create/connect to a SQLite database
    database_connection = sqlite3.connect('stock_data.db')
    db_cursor = database_connection.cursor()

    # Create the stocks table if it doesn't exist
    db_cursor.execute('''CREATE TABLE IF NOT EXISTS stock_info (
                            id INTEGER PRIMARY KEY,
                            stock_code TEXT,
                            stock_name TEXT,
                            stock_price REAL,
                            price_change REAL,
                            price_change_percent REAL,
                            volume INTEGER,
                            turnover REAL,
                            amplitude REAL,
                            highest REAL,
                            lowest REAL,
                            open_price REAL,
                            last_close REAL
                        )''')

    for stock in stocks_data:
        # Parse stock data
        stock_info = {}
        attributes = stock.split(',')

        for attribute in attributes:
            key_value = attribute.split(':')
            key = key_value[0].strip('"')
            value = key_value[1].strip('"')
            stock_info[key] = value

        # Extract relevant stock information
        stock_code = stock_info.get('f12', 'N/A')
        stock_name = stock_info.get('f14', 'N/A')
        stock_price = float(stock_info.get('f2', 0.0))
        price_change = float(stock_info.get('f4', 0.0))
        price_change_percent = float(stock_info.get('f3', 0.0))
        volume = int(stock_info.get('f5', 0))
        turnover = float(stock_info.get('f6', 0.0))
        amplitude = float(stock_info.get('f7', 0.0))
        highest = float(stock_info.get('f15', 0.0))
        lowest = float(stock_info.get('f16', 0.0))
        open_price = float(stock_info.get('f17', 0.0))
        last_close = float(stock_info.get('f18', 0.0))

        # Insert stock data into the database
        db_cursor.execute(
            "INSERT INTO stock_info (stock_code, stock_name, stock_price, price_change, price_change_percent, volume, turnover, amplitude, highest, lowest, open_price, last_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (stock_code, stock_name, stock_price, price_change, price_change_percent, volume, turnover, amplitude,
             highest, lowest, open_price, last_close))

        database_connection.commit()

    # Query all stock data
    db_cursor.execute("SELECT * FROM stock_info")
    all_stocks = db_cursor.fetchall()

    # Get column names for displaying data
    column_names = [description[0] for description in db_cursor.description]
    print("\t".join(column_names))

    # Display each stock's information
    for stock in all_stocks:
        print("\t".join(map(str, stock)))

    # Close the database connection
    database_connection.close()


# Execute the function with specified parameters
page_number = 1
process_stock_data("fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048", page_number)
