from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

url = Request(
    'https://en.wikipedia.org/wiki/Tariffs_in_the_second_Trump_administration#:~:text=From%20January%20to%20April%202025,level%20in%20over%20a%20century.&text=Trump%20escalated%20an%20ongoing%20trade,%25%20after%20April%209%2C%202025.',
    headers=headers
)

page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode('utf-8')
#print(html)

soup = BeautifulSoup(html, "lxml")

tables = soup.find_all("table")

with pd.ExcelWriter("extracted_tables_wikipedia.xlsx", engine="openpyxl") as writer:
    for idx, table in enumerate(tables):
        rows = table.find_all("tr")
        data = []

        for row in rows:
            cols = row.find_all(['td', 'th'])
            cols = [col.get_text(strip=True) for col in cols]
            data.append(cols)
            
        df = pd.DataFrame(data)
        
        df.to_excel(writer, sheet_name = f"Table_{idx + 1}", index=False, header=False)

        # test