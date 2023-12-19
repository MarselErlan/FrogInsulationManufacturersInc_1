import requests
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
import requests

url = 'https://jobes-nextjs.vercel.app/job-details'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Accept': 'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8',

    # ... другие заголовки, если они нужны
}

response = requests.get(url, headers=headers)
html_content = response.text

with open('saved_page3.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("Страница сохранена в 'saved_page.html'")










