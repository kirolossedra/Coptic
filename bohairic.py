from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_bohairic(sahidic_word):
    # Construct target URL with sahidic word
    url = f"https://remnqymi.com/crum/?query={sahidic_word}&full=true"

    # Configure Chrome headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Start Chrome
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for JS/animations to finish
    time.sleep(1)

    # Get final rendered HTML
    final_html = driver.page_source
    #print(final_html)

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(final_html, 'html.parser')

    # Extract Bohairic spelling
    bohairic = "Not found"
    table = soup.find('table', id='crum', class_='results')
    if table:
        tbody = table.find('tbody')
        if tbody:
            for row in tbody.find_all('tr'):
                tds = row.find_all('td')
                if len(tds) >= 2:
                    # Look for mixed dialects containing B first (e.g., "A B S spelling", "B S spelling", "A B spelling")
                    mixed_spelling = tds[1].find('span', class_=lambda x: x and 'spelling' in x and 'B' in x.split())
                    if mixed_spelling and mixed_spelling.text.strip():
                        bohairic = mixed_spelling.text.strip()
                        break
                    # If no mixed dialect found, look for B alone
                    b_spelling = tds[1].find('span', class_='B spelling')
                    if b_spelling and b_spelling.text.strip():
                        bohairic = b_spelling.text.strip()
                        break

    driver.quit()
    
    return bohairic

# Example usage:
result = get_bohairic("ⲛⲟⲩⲣⲉ")
print(f"Bohairic: {result}")
