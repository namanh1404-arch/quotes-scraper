import time
import csv
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "http://quotes.toscrape.com"
output_file = "quotes.csv"
request_delay = 1

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scraper.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

def fetch_page(url):
    logger.info(f"Crawling: {url}")
    response = requests.get(url, timeout=10)
    logger.info(f"Success: {url} (status {response.status_code})")
    return response.text

def parse_quotes(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes = []

    for quote_div in soup.find_all("div", class_="quote"):
        author = quote_div.find("small", class_="author")
        text = quote_div.find("span", class_="text")

        quotes.append({
            "author": author.text.strip(),
            "text": text.text.strip(),
        })

    logger.info(f"Parsed {len(quotes)} quotes")
    return quotes

def find_next_page(html):
    soup = BeautifulSoup(html, "html.parser")
    next_button = soup.find("li", class_="next")

    if not next_button: return None

    next_link = next_button.find("a")
    if not next_link or "href" not in next_link.attrs:
        return None
    
    return urljoin(base_url, next_link["href"])

def save_to_csv(quotes, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file) # Tạo object writer để ghi từng dòng vào file.
        writer.writerow(["No.", "Author", "Quote"])
        for index, quote in enumerate(quotes, start=1):
            writer.writerow([index, quote["author"], quote["text"]])

def main():
    all_quotes = []
    url = base_url

    while url:
        html = fetch_page(url)

        quotes = parse_quotes(html)
        all_quotes.extend(quotes)

        url = find_next_page(html)
        if url:
            time.sleep(request_delay)
    
    save_to_csv(all_quotes, output_file)


if __name__ == "__main__":
    main()