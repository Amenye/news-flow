#%%
###CREATING THE SCRAPER###

#Importing the necessary libraries
import enum
import requests
from bs4 import BeautifulSoup
import time
import random

#Fetching(getting the data)
TARGET_URL = "https://news.ycombinator.com/"

def fetch_html(url):
    """
    Fetches the raw HTML content from URL.
    Includes 'User-Agent' to avoid being blocked.
    """
    # User-Agent: Pretend to be a real browser, not a bot script
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers = headers, timeout = 10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"⚠️Network Error: {e}")
        return None


#%%
#Parsing the data
def parse_articles(html_content):
    """
    Parse the HTML to extract article data.
    Returns: Liost of dictionaries
    """
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, "html.parser")
    articles = []

    #Hacker News styructure relies on ,<tr class="athing"> for headlines
    rows = soup.find_all("tr", class_="athing")

    for row in rows:
        try:
            #Extract Title and Link
            title_element = row.find("span", class_="titleline").find("a")
            title = title_element.get_text()
            link = title_element["href"]

            #Extract the Source Domain
            site_span = row.find("span", class_="sitestr")
            source = site_span.get_text() if site_span else "Hacker News"

            #Clean up the data immediately
            article_data = {
                "title": title,
                "url": link,
                "source": source
            }
            articles.append(article_data)

        except AttributeError:
            #If a row is malformed skip it rather than crashing
            continue

    return articles


#%%
#function to scrap the news website
def scrape_news():
    """
    Orchestrator function to fetch and parse.
    """
    print(f"Fetching news from {TARGET_URL}...")
    html = fetch_html(TARGET_URL)

    if html:
        data = parse_articles(html)
        print(f"Successfully scraped {len(data)} articles.")
        return data
    else:
        print("⚠️Failed to retreive data")
        return []


#%%
#TEST BLOCK
#Testing the code
if __name__ == "__main__":
    scraped_data = scrape_news()

    for i, item in enumerate(scraped_data[:3], 1):
        print(f"{i}. [{item['source']}] {item['title']}")
#%%