import requests
from bs4 import BeautifulSoup
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
import re
import sqlite3
# driver = webdriver.Firefox()

# main_site = driver.get('https://www.riktkurs.nu/')

'''
base_url = (
    "https://www.riktkurs.nu/senaste"  # will be extractwd from a database list of urls
)
keyword = ""
website = requests.get(base_url)

soup = BeautifulSoup(website.text, "html.parser")

print(soup.title.string)

href_list = []

for link in soup.find_all("a"):  # Find all <a> tags
    href = link.get("href")  # Get the href attribute
    if href:  # Ensure href exists (to skip empty ones)
        # print(href)
        href_list.append(href)


# print(href_list)

# Access and save raw hyper links
hyper_link_list = []

for h in href_list:
    normalized_base = base_url.lstrip("/senaste")
    hyper_link = normalized_base + h
    hyper_link_list.append(hyper_link)
#    print(hyper_link)
# print(hyper_link_list)

# filter hypeelinks based on content
# Itterate through hyper_link_list, accessing each' html and regmatching for keyword

stock_pages = []
checks = 0
for l in hyper_link_list:
    checks += 1
    print(checks)
    page = requests.get(l)
    page_soup = BeautifulSoup(page.text, "html.parser")

    pattern = re.compile("SEK")
    matches = pattern.findall(page.text)
    if len(matches) > 0:
        #    stock_pages.append(l)
        print("Append", l)
print(stock_pages)
'''

con = sqlite3.connect("tradingtool.db")
cur = con.cursor()

#cur.execute("CREATE TABLE main(src_name, src_url, trgt_url)")

res = cur.execute("SELECT name FROM sqlite_master")
result = res.fetchall()
print(result)


cur.execute("""
    INSERT INTO main VALUES 
            ('riktkurser.se', 'https://www.riktkurs.nu/senaste/', 'https://www.riktkurs.nu/')
            """)
con.commit()



