import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#driver = webdriver.Firefox()

#main_site = driver.get('https://www.riktkurs.nu/')

base_url = 'https://www.riktkurs.nu/' # will be extractwd from a database list of urls
website = requests.get(base_url)

soup = BeautifulSoup(website.text, 'html.parser')

print(soup.title.string)

href_list = [];

for link in soup.find_all('a'):  # Find all <a> tags
    href = link.get('href')     # Get the href attribute
    if href:                    # Ensure href exists (to skip empty ones)
        #print(href)
        href_list.append(href)


print(href_list)

# Access and save raw hyper links
hyper_link_list = [];

for h in href_list:
    nomralized_h = h.lstrip("/");
    hyper_link = base_url + nomralized_h
    nomralized_hyper_link = hyper_link + "/";
    hyper_link_list.append(nomralized_hyper_link);
    #print(hyper_link)
print(hyper_link_list)

# filter hypeelinks based on content
# to be done from a separet class script

