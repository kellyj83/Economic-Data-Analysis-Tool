from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests
from io import StringIO
import json

'''headers = {
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
'''
        
def extract_links(soup):
    links = []
    for link in soup.find_all("a", href=True):
        url = link["href"]
        
        if not url.startswith("http"):
            url = "<https://en.wikipedia.org>" + url
            links.append(url)
        return links
    

def extract_paragraphs(soup):
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    return [p for p in paragraphs if p and len(p)>10]

def extract_tables(soup):
    tables = []

    for table in soup.find_all("table", {"class": "wikitable"}):
        table_html = StringIO(str(table))
        df = pd.read_html(table_html)[0]
        tables.append(df)
    
    return tables


def store_data(links, tables, paragraphs):
    with open("wikipedia_links.txt", "w", encoding="utf-8") as f:
        for link in links:
            f.write(f"{link}\\n")

    with open("wikipedia_paragraphs.txt", "w", encoding="utf-8") as f:
        for para in paragraphs:
            f.write(f"{para}\\n\n")

    for i, table in enumerate(tables):
        table.to_csv(f"wikipedia_table_{i+1}.csv", index=False, encoding="utf-8-sig")


def scrape_wikipedia(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = extract_links(soup)
    tables = extract_tables(soup)
    paragraphs = extract_paragraphs(soup)

    store_data(links, tables, paragraphs)


scrape_wikipedia("https://en.wikipedia.org/wiki/Tariffs_in_the_second_Trump_administration")



##### NEXT STEP: Get the ChatGPT API that can summarise paragraph data into economic data 
#### Convert the wiki tables into accurate data that we can extract from 
#### Maybe use it and connect an API that can build a graph/chart of all the tariffs so one can easily visualise them