import re
import os
import requests

# Step 1: 获取网页HTML源码并存储在变量中
def get_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text  # 将源代码存储在一个变量中
            return html_content  # 返回网页的HTML内容
        else:
            print(f"无法获取网页内容，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求网页失败: {e}")
        return None

# Step 2: 提取并解码 MP3 链接
def extract_and_decode_mp3_links(html):
    # 匹配所有带有 .mp3 的链接，保持顺序
    mp3_pattern = r'https:\\u002F\\u002Fuploadstatic\.mihoyo\.com\\u002Fys-obc\\u002F.*?\.mp3'
    raw_links = re.findall(mp3_pattern, html)

    # 解码 Unicode 字符，例如 \u002F 代表 /
    decoded_links = [link.encode('utf-8').decode('unicode_escape') for link in raw_links]

    # 提取前四分之一的链接（假设中文是前四分之一）
    quarter_length = len(decoded_links) // 4
    selected_links = decoded_links[:quarter_length]
    
    return selected_links

# Step 3: 下载 MP3 文件
def download_mp3(mp3_links, folder="MP3"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for index, link in enumerate(mp3_links):
        mp3_filename = os.path.join(folder, f"file_{index + 1}.mp3")
        try:
            response = requests.get(link)
            with open(mp3_filename, 'wb') as f:
                f.write(response.content)
            print(f"下载成功: {mp3_filename}")
        except Exception as e:
            print(f"下载失败: {link}，错误信息: {e}")

# 主函数
def main(url):
    # Step 1: 获取网页HTML
    html = get_html(url)
    if not html:
        return

    # Step 2: 提取并解码 MP3 链接
    mp3_links = extract_and_decode_mp3_links(html)
    if mp3_links:
        print(f"发现 {len(mp3_links)} 个 MP3 链接:")
        for link in mp3_links:
            print(link)
    else:
        print("未找到符合条件的 MP3 链接")

    # Step 3: 下载 MP3 文件
    download_mp3(mp3_links)

# 运行代码：输入目标网页的 URL
url = input("请输入网页URL: ")
main(url)
