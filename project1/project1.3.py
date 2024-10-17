import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 设置目标网页和保存路径
url = 'https://news.fzu.edu.cn/yxfd.htm'
save_dir = r'E:\数据采集实践projects\project1\Image'

# 创建保存目录（如果不存在）
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 函数：下载图片
def download_image(image_url):
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()  # 检查请求是否成功
        with open(os.path.join(save_dir, os.path.basename(image_url)), 'wb') as f:
            f.write(response.content)
        print(f"下载成功: {image_url}")
    except Exception as e:
        print(f"下载失败: {image_url}. 错误: {e}")

# 获取网页内容
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有JPEG和JPG格式的图片
    img_tags = soup.find_all('img')
    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            # 确保URL是完整的
            img_url = urljoin(url, img_url)
            if img_url.lower().endswith(('.jpeg', '.jpg')):
                download_image(img_url)

except Exception as e:
    print(f"无法访问网页: {url}. 错误: {e}")
