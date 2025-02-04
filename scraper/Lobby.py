from RecursiveScraper import RecursiveScraper

key_words = {
    1: ["a", "LatestRecommendationsForStockPerRecommender"],
    0: ["a", "LatestRecommendationsForStockPerRecommender"],
}  # key-intuition = distance to target, all elements with keys > 0 list sub_page filters.
# url = input()
url = "https://www.riktkurs.nu/"

riktskurs_scraper = RecursiveScraper()

results = riktskurs_scraper.scrap(key_words, base_url=url)

print(len(results))