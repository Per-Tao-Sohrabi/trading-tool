import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from urllib.parse import urljoin

class RecursiveScraping:

    def __init__(self, key_words_dict = None, base_url = None):
        self.key_words = key_words_dict

        self.recursions = len(self.key_words)-1 # len = 1. # declare number of recursive steps.

        self.super_url = base_url

        self.result = []

        pass
    
    def scrap(self):
        self.recursiveScraping(url = self.super_url, recursions = self.recursions, key_words = self.key_words)
        return self.result

    # RECURSIVE SCRAPING MECHANISM
    def recursiveScraping(self, url = "", recursions = None, key_words = {}, tot_recur = None):
        # Normalize url
        base_url = url.rstrip("/")
        
        # Super case
        if(tot_recur == None):
            tot_recur = recursions; # tot_recur = recur 1. 
            print("Total recurrsions identified: ", tot_recur)
        
        # distancet to base page
        distance = recursions
        print("Distance to base case: ", distance)
        
        # Isolate keyword at current level
        keyword_hash = key_words[distance] # Observed the current base keyword dictionary at the end of the keywords list. 
        print("Sub page regex filters: ", keyword_hash)

        # Base case
        if(recursions == 0):
            print("At base page: ", base_url)
            
            page = requests.get(url)
            
            page_soup = BeautifulSoup(page.text, 'html.parser')
            
            target_element_lines = page_soup.find_all(keyword_hash[0], re.compile(keyword_hash[1]))

            output = [url, target_element_lines]
            
            self.result.append(output)
            
        # Reccursive case, aims to filter through sub_urls to get to the base url
        if(recursions>0):

            # update recursion
            recursions -= 1
            
            # retrive next url
            current_page = requests.get(url)
            current_page_soup = BeautifulSoup(current_page.text, 'html.parser')

            # identify and filter sub-urls
            hyperlinks = []
            for a_element in  current_page_soup.find_all('a'): # filters through all <a> elements on the page. 
                href = a_element.get('href'); #extract the href term in a_element.

                # concatenate complete url
                hyperlink = self.normalize_href(base_url, href) #extract the full hyperlink
                
                # store hyperlink
                hyperlinks.append(hyperlink)
                print("Identifyied hyperlink: ", hyperlink)

            # filter through hyperlinks
            filtered_hyperlinks = []
            for l in hyperlinks:

                # Access the sub_page
                sub_page = requests.get(l)
                sub_soup = BeautifulSoup(sub_page.text, 'html.parser')

                # Check for keyword
                result = sub_soup.find_all(keyword_hash[0], class_=re.compile(keyword_hash[1])) 
                
                # Save link if 
                print("Judjing hyperlink: ",l)
                #print(f'key element: {keyword_hash[0]}, key word: {keyword_hash[1]}, result: {result}')
                if len(result) > 0:
                    filtered_hyperlinks.append(l) #append 
                    print("Hyperlink accepted")
                else:
                    print("Hyperlink rejected")
            
            for hyperlink in filtered_hyperlinks:
                self.recursiveScraping(url=hyperlink, recursions= recursions, key_words= key_words, tot_recur=tot_recur)

    # HELPER FUNCTION
    def normalize_href(self, base_url = "", href = ""):
        if href.startswith("http"):  # Absolute URL (No change needed)
                full_url = href
                link_type = "Absolute URL"
        elif href.startswith("//"):  # Protocol-relative URL
            full_url = base_url.split(":")[0] + ":" + href
            link_type = "Protocol-relative"
        elif href.startswith("/"):  # Root-relative URL
            full_url = urljoin(base_url, href)
            link_type = "Root-relative"
        elif href.startswith("./"):  # Current directory relative
            full_url = urljoin(base_url, href[2:])  # Remove "./"
            link_type = "Current directory relative"
        elif href.startswith("../"):  # Parent directory relative
            full_url = urljoin(base_url, href)
            link_type = "Parent directory relative"
        else:  # Other cases (relative without `.` or `/`)
            full_url = urljoin(base_url + "/", href)
            link_type = "Other relative"
        
        return full_url

key_words = {1:["a","LatestRecommendationsForStockPerRecommender"], 0:["a","LatestRecommendationsForStockPerRecommender"]} # key-intuition = distance to target, all elements with keys > 0 list sub_page filters.

url = "https://www.riktkurs.nu/"

riktskurs_scraper = RecursiveScraping(key_words, base_url=url)

results = riktskurs_scraper.scrap()

print(len(results))
