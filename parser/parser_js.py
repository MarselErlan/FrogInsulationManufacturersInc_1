# import requests
# from bs4 import BeautifulSoup
# import os
#
# url = 'https://jobes-nextjs.vercel.app/'
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
#     'Accept': 'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8',
# }
#
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# # Находим все теги <script> с атрибутом src
# scripts = soup.find_all('script', src=True)
#
# if not os.path.exists('js_files'):
#     os.makedirs('js_files')
#
# for script in scripts:
#     src_url = script['src']
#     # Если src не содержит полного URL, дополняем его
#     if not src_url.startswith('http'):
#         src_url = requests.compat.urljoin(url, src_url)
#
#     js_content = requests.get(src_url, headers=headers).text
#     js_filename = os.path.join('js_files', os.path.basename(src_url))
#
#     with open(js_filename, 'w', encoding='utf-8') as js_file:
#         js_file.write(js_content)
#
# print(f"{len(scripts)} JS файлов сохранено в папке 'js_files'")
import requests
from bs4 import BeautifulSoup
import os

url = 'https://jobes-nextjs.vercel.app/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Accept': 'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8',
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все теги <link> с атрибутом href, которые предназначены для prefetch'ing
links = soup.find_all('link', {'rel': 'prefetch'}, href=True)

if not os.path.exists('js_files'):
    os.makedirs('js_files')

for link in links:
    href_url = link['href']
    # Если href не содержит полного URL, дополняем его
    if not href_url.startswith('http'):
        href_url = requests.compat.urljoin(url, href_url)

    js_content = requests.get(href_url, headers=headers).text
    js_filename = os.path.join('js_files', os.path.basename(href_url))

    with open(js_filename, 'w', encoding='utf-8') as js_file:
        js_file.write(js_content)

print(f"{len(links)} JS файлов сохранено в папке 'js_files'")
