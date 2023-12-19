import requests
from bs4 import BeautifulSoup
import os

url = 'https://www.generalinsulation.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Accept': 'text/css,*/*;q=0.1',
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Собираем все изображения
images = soup.find_all('img', src=True)

if not os.path.exists('../media_files'):
    os.makedirs('../media_files')

for img in images:
    src_url = img['src']
    if not src_url.startswith('http'):
        src_url = requests.compat.urljoin(url, src_url)

    img_data = requests.get(src_url, headers=headers).content
    img_filename = os.path.join('../media_files', os.path.basename(src_url))

    with open(img_filename, 'wb') as img_file:
        img_file.write(img_data)

print(f"{len(images)} медиафайлов сохранено в папке 'media_files'")
