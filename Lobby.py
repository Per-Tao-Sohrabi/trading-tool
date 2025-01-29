from RecursiveScraper import RecursiveScraper

key_words = {1:["a","LatestRecommendationsForStockPerRecommender"], 0:["a","LatestRecommendationsForStockPerRecommender"]} # key-intuition = distance to target, all elements with keys > 0 list sub_page filters.

url = "https://www.riktkurs.nu/"

riktskurs_scraper = RecursiveScraper(key_words, base_url=url)

results = riktskurs_scraper.scrap()

print(len(results))