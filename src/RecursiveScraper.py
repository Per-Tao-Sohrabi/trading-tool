import requests
from bs4 import BeautifulSoup
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
import re
from urllib.parse import urljoin


class RecursiveScraper:

    def __init__(self):  #self, key_words_dict=None, base_url=None
        '''
        Initiates a RecursiveScraper object. 
        Param:
        - vars: 
            - self.write: boolean, --> affects self.print_out()
            - self.result: [] --> outputspace for recursive scraping.

        - args: N/A
        - return: N/A
        '''
        self.write = False
        self.result = []
        pass

    def scrap(self, key_words_dict=None, source_url=None, base_url=None, write=False):
        self.write = write
        self.result.clear();
        recursions = (len(key_words_dict) - 1)  # len = 1. # declare number of recursive steps.
        
        self.recursiveScraping(
            source_url=source_url, base_url=base_url, recursions=recursions, key_words=key_words_dict
        )
        return self.result # Output contains [ source_url, [html tag-lines] ]

    # RECURSIVE SCRAPING MECHANISM
    def recursiveScraping(self, source_url=None, base_url=None, recursions=None, key_words={}, tot_recur=None):
        

        # Retrive current page soup
        current_page = requests.get(source_url)
        current_page_soup = BeautifulSoup(current_page.text, "html.parser")
            

        # Super case
        if tot_recur == None:
            tot_recur = recursions
            source_url = base_url
            self.print_out("Total recurrsions identified: ", tot_recur)

        # Calculate distancet to base page
        distance = recursions
        self.print_out("Distance to base case: ", distance)

        # Isolate keyword at current level
        keyword_hash = key_words[
            str(distance)
        ]  # Observed the current base keyword dictionary at the end of the keywords list.
        self.print_out("Sub page regex filters: ", keyword_hash)

        # Normalize url
        source_url_url = source_url.rstrip("/")
        
        # Base case
        if recursions == 0:
            self.print_out("At base page: ", source_url)

            target_element_lines = current_page_soup.find_all(
                keyword_hash[0], re.compile(keyword_hash[1])
            )
            str_target_element_lines = [str(item) for item in target_element_lines]

            output = {source_url: str_target_element_lines} #CHANGE

            self.result.append(output)

        # Reccursive case, aims to filter through sub_urls to get to the base url
        if recursions > 0:

            # update recursion
            recursions -= 1

            # identify and filter sub-urls
            hyperlinks = []
            for a_element in current_page_soup.find_all("a"):  # filters through all <a> elements on the page.
                
                href = a_element.get("href") # extract the href term in a_element.
                
                # concatenate complete url
                hyperlink = self.normalize_href(
                    source_url, href
                )  # extract the full hyperlink

                # store hyperlink
                hyperlinks.append(hyperlink)
                self.print_out("Identifyied hyperlink: ", hyperlink)

            # filter through hyperlinks
            filtered_hyperlinks = []
            for l in hyperlinks:
                # Access the sub_page
                sub_page = requests.get(l)
                sub_soup = BeautifulSoup(sub_page.text, "html.parser")

                # Check for keyword
                result = sub_soup.find_all(
                    keyword_hash[0], class_=re.compile(keyword_hash[1])
                )

                # Save link if
                self.print_out("Judjing hyperlink: ", l)
                # self.print_out(f'key element: {keyword_hash[0]}, key word: {keyword_hash[1]}, result: {result}')
                if len(result) > 0:
                    filtered_hyperlinks.append(l)  # append
                    self.print_out("Hyperlink accepted")
                else:
                    self.print_out("Hyperlink rejected")

            for hyperlink in filtered_hyperlinks:
                self.recursiveScraping(
                    source_url=hyperlink,
                    recursions=recursions,
                    key_words=key_words,
                    tot_recur=tot_recur,
                )

    # HELPER FUNCTION
    def normalize_href(self, source_url="", href=""):
        if href.startswith("http"):  # Absolute URL (No change needed)
            full_url = href
            link_type = "Absolute URL"
        elif href.startswith("//"):  # Protocol-relative URL
            full_url = source_url.split(":")[0] + ":" + href
            link_type = "Protocol-relative"
        elif href.startswith("/"):  # Root-relative URL
            full_url = urljoin(source_url, href)
            link_type = "Root-relative"
        elif href.startswith("./"):  # Current directory relative
            full_url = urljoin(source_url, href[2:])  # Remove "./"
            link_type = "Current directory relative"
        elif href.startswith("../"):  # Parent directory relative
            full_url = urljoin(source_url, href)
            link_type = "Parent directory relative"
        else:  # Other cases (relative without `.` or `/`)
            full_url = urljoin(source_url + "/", href)
            link_type = "Other relative"

        return full_url


    def print_out(self, *args):
        if self.write == True:
            output = ""
            for arg in range(args):
                output = output + str(arg)

            return output


# MAIN
'''
key_words = {
    1: ["a", "LatestRecommendationsForStockPerRecommender"],
    0: ["a", "LatestRecommendationsForStockPerRecommender"],
}  # key-intuition = distance to target, all elements with keys > 0 list sub_page filters.

url = "https://www.riktkurs.nu/"

riktskurs_scraper = RecursiveScraper(key_words, base_url=url)

results = riktskurs_scraper.scrap()

self.print_out(len(results))
'''