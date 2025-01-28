import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#driver = webdriver.Firefox()

#main_site = driver.get('https://www.riktkurs.nu/')

base_url = 'https://www.riktkurs.nu/'
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

# Create new links
target_link_list = [];

for h in href_list:
    nomralized_h = h.lstrip("/");
    target_link = base_url + nomralized_h
    nomralized_target_link = target_link + "/";
    target_link_list.append(nomralized_target_link);
    #print(target_link)

print(target_link_list)