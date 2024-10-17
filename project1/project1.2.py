import requests
from bs4 import BeautifulSoup


# 函数：获取指定URL的页面内容
def fetch_page(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # 检查请求是否成功
        response.encoding = response.apparent_encoding
        return response.text
    except requests.RequestException as error:
        print(f"请求失败: {error}")
        return None


# 函数：提取产品名称和价格
def extract_product_details(html_content):
    if html_content is None:
        return []

    soup = BeautifulSoup(html_content, 'lxml')
    product_info_list = []

    # 查找所有商品列表项
    product_items = soup.find_all('li')

    for product in product_items:
        try:
            # 获取产品名称
            title_tag = product.find('a', attrs={'dd_name': '单品图片'})
            product_name = title_tag['title'].strip() if title_tag else None

            # 获取产品价格
            price_tag = product.find('span', class_='price_n')
            product_price = price_tag.text.strip() if price_tag else None

            if product_name and product_price:
                product_info_list.append((product_name, product_price))  # 添加到列表

        except Exception:
            continue  # 跳过异常，继续处理下一个条目

    return product_info_list


# 函数：打印产品信息
def display_product_info(products):
    print('序号\t价格\t商品名称')
    print('-' * 50)  # 打印分隔线
    for index, (name, price) in enumerate(products, start=1):
        print(f"{index}\t{price}\t{name}")
        print('-' * 50)  # 每行后打印分隔线


# 主程序执行入口
if __name__ == '__main__':
    search_url = 'https://search.dangdang.com/?key=%CA%E9%B0%FC&act=input'
    request_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
    }

    # 获取页面内容
    content = fetch_page(search_url, request_headers)
    # 解析产品详情
    products = extract_product_details(content)
    # 显示产品信息
    display_product_info(products)


