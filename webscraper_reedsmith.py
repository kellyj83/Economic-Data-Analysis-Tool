from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

url = Request(
    'https://www.tradecomplianceresourcehub.com/2025/04/11/trump-2-0-tariff-tracker/',
    headers=headers
)

page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode('utf-8')
#print(html)

soup = BeautifulSoup(html, "lxml")

tables = soup.find_all("table")

with pd.ExcelWriter("extracted_tables.xlsx", engine="openpyxl") as writer:
    for idx, table in enumerate(tables):
        rows = table.find_all("tr")
        data = []

        for row in rows:
            cols = row.find_all(['td', 'th'])
            cols = [col.get_text(strip=True) for col in cols]
            data.append(cols)
            
        df = pd.DataFrame(data)
        
        df.to_excel(writer, sheet_name = f"Table_{idx + 1}", index=False, header=False)