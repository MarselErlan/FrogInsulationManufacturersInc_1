import requests
from bs4 import BeautifulSoup
import os

url = 'https://jobes-nextjs.vercel.app/index3'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Accept': 'text/css,*/*;q=0.1',
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все теги <link> с атрибутом href и rel равным "stylesheet"
stylesheets = soup.find_all('link', href=True, rel=lambda x: x and 'stylesheet' in x)

if not os.path.exists('css_files'):
    os.makedirs('css_files')

for stylesheet in stylesheets:
    href_url = stylesheet['href']
    # Если href не содержит полного URL, дополняем его
    if not href_url.startswith('http'):
        href_url = requests.compat.urljoin(url, href_url)

    css_content = requests.get(href_url, headers=headers).text
    css_filename = os.path.join('css_files', os.path.basename(href_url))

    with open(css_filename, 'w', encoding='utf-8') as css_file:
        css_file.write(css_content)

print(f"{len(stylesheets)} CSS файлов сохранено в папке 'css_files'")
