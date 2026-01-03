#%%
#Importing the necessary libraries
from pdb import run
import sys
from src.database import create_tables, insert_article
from src.scraper import scrape_news
from src.cleaner import clean_text, validate_article

def run_pipeline():
    print('Starting NewsFlow Pipeline....')

    #1. Ensure the DB exists
    create_tables()

    #2. Fetch Data
    raw_articles = scrape_news()
    if not raw_articles:
        print("⚠️No articles were found")
        return

    print(f"Processing {len(raw_articles)} articles...")
    stats = {"new": 0, "duplicate": 0, "invalid": 0}

    #3. Process and Save
    for article in raw_articles:
        #Validation
        if not validate_article(article):
            stats["invalid"] += 1
            continue

        #Cleaning
        title = clean_text(article['title'])
        url = article['url']
        source = clean_text(article['source'])

        #Ingestion
        saved = insert_article(title, url, source)

        if saved:
            stats["new"] += 1
        else:
            stats["duplicate"] += 1
        

    # 4. Final Report
    print("\n📊 --- PIPELINE SUMMARY ---")
    print(f"✅ Added:      {stats['new']}")
    print(f"⚠️ Duplicates: {stats['duplicate']}")
    print(f"❌ Invalid:    {stats['invalid']}")
    print("-------------------------")

if __name__ == "__main__":
    run_pipeline()

#%%
