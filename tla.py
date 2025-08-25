import requests
from bs4 import BeautifulSoup
import sys

def get_hieroglyphs(url):
    """
    Scrapes the TLA lemma page for the hieroglyphic spelling.
    Returns the hieroglyph from 'lemma-property-hieroglyphs' div if found.
    Otherwise, returns the first valid hieroglyph from 'lemma-spellings' div.
    
    Args:
        url (str): The URL of the lemma page.
    
    Returns:
        str: The hieroglyph as a string, or 'No hieroglyphs found' if none available.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching page: {e}"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check for primary hieroglyph in lemma-property-hieroglyphs
    primary_div = soup.find('div', id='lemma-property-hieroglyphs')
    if primary_div:
        span = primary_div.find('span', class_='unicode-hieroglyphs')
        if span and span.text.strip():
            return span.text.strip()
    
    # If not found, get the first valid hieroglyph from lemma-spellings
    spellings_div = soup.find('div', id='lemma-spellings')
    if spellings_div:
        spans = spellings_div.find_all('span', class_='unicode-hieroglyphs')
        for span in spans:
            text = span.text.strip()
            if text and text != '∅':
                return text
    
    return 'No hieroglyphs found'

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrape_tla_hieroglyphs.py <TLA_lemma_URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    print(get_hieroglyphs(url))
