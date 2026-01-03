#%%
#Importing the necessary library
import re

#Cleaning the text to standardize it
def clean_text(text):
    """
    Standardizes text data:
    1. Removes leading/trailing whitespace
    2. Collapses multiple spaces into one
    3. (Optional) Converts to lowercase for consistent analysis
    """
    if not text:
        return None

    # "  BreakING   News!  " -> "BreakING News!"
    cleaned = text.strip()
    
    # "Hello    World" -> "Hello World"
    cleaned = re.sub(r'\s+', ' ', cleaned)

    return cleaned


#%%
#Validating the article
def validate_article(article):
    """
    Checking if the article has the minimun required data.
    Returns: True if valid, False otherwise
    """
    if not article.get("title") or not article.get("url"):
        return False

    #Basic URL validation (must start wit 'http')
    if not article['url'].startswith('http'):
        return False
    
    return True
#%%