import requests
from bs4 import BeautifulSoup
import sys

print("Starting script...")

if len(sys.argv) < 2:
    print("Usage: python script.py <url>")
    sys.exit(1)

url = sys.argv[1]
print(f"Fetching URL: {url}")

try:
    response = requests.get(url)
    print("Request completed. Status code:", response.status_code)
except Exception as e:
    print("Error during request:", str(e))
    sys.exit(1)

if response.status_code != 200:
    print("Failed to fetch page")
    sys.exit(1)

print("Parsing HTML...")
soup = BeautifulSoup(response.text, 'html.parser')
print("HTML parsed.")

# Extract orthographies
print("Extracting orthographies...")
orth_dict = {}
for td in soup.find_all('td', class_='dialect'):
    print("Found dialect td")
    row = td.parent
    if row.name == 'tr':
        orth_td = row.find('td', class_='orth_entry')
        if orth_td and orth_td.text.strip():
            dialect = td.text.strip()
            orth = orth_td.text.strip()
            orth_dict[dialect] = orth
            print(f"Added {dialect}: {orth}")
print("Orthographies extraction complete.")

# Extract Hieroglyphic Egyptian etymology
print("Extracting etymology...")
etym_div = soup.find('div', id='etym')
hiero_etym = 'Not found'
hiero_id = 'Not found'
if etym_div:
    print("Found etym div")
    eg_etym = etym_div.find('span', class_='eg_etym')
    if not eg_etym:
        eg_etym = etym_div
        print("Using etym_div as eg_etym")
    text = eg_etym.text.strip()
    print(f"Etym text: {text}")
    if 'Hieroglyphic Egyptian' in text:
        print("Found 'Hieroglyphic Egyptian'")
        parts = text.split('Hieroglyphic Egyptian')
        if len(parts) > 1:
            after = parts[1].split('see TLA:')[0].strip()
            if after.endswith(';'):
                after = after[:-1].strip()
            hiero_etym = after
            print(f"Extracted hiero_etym: {hiero_etym}")
    tla_hiero_link = etym_div.find('a', string=lambda s: s and 'Hieroglyphic Egyptian' in s)
    if tla_hiero_link:
        print("Found tla_hiero_link")
        href = tla_hiero_link['href']
        print(f"Href: {href}")
        if '/lemma/' in href:
            hiero_id = href.split('/lemma/')[1].strip('"]')
            print(f"Extracted hiero_id: {hiero_id}")
print("Etymology extraction complete.")

# Extract meanings
print("Extracting meanings...")
meanings = []
senses_table = soup.find('table', id='senses')
if senses_table:
    print("Found senses table")
    for tr in senses_table.find_all('tr', recursive=False):
        print("Processing tr")
        entry_num = tr.find('td', class_='entry_num')
        if entry_num:
            print("Found entry_num")
            lang_td = tr.find('td', class_='sense_lang')
            trans_td = tr.find('td', class_='trans')
            if lang_td and trans_td and lang_td.text.strip() == '(En)':
                print("Found English trans")
                meaning = trans_td.text.strip()
                if 'see TLA:' in meaning:
                    meaning = meaning.split('see TLA:')[0].strip()
                meanings.append(meaning)
                print(f"Added meaning: {meaning}")
else:
    print("No senses table found")
print("Meanings extraction complete.")

# Output
print("Generating output...")
sahidic = orth_dict.get('S', 'Not found')
print(f"Sahidic: {sahidic}")

bohairic = orth_dict.get('B', None)
if bohairic:
    print(f"Bohairic: {bohairic}")

other_dialects = {k: v for k, v in orth_dict.items() if k not in ['S', 'B']}
if other_dialects:
    print("Other dialects:")
    for d, o in other_dialects.items():
        print(f"  {d}: {o}")

print(f"Hieroglyphic Egyptian Etymology: {hiero_etym}")
print(f"TLA ID: {hiero_id}")

if meanings:
    print("Meanings:")
    for i, m in enumerate(meanings, 1):
        print(f"({i}) {m}")
else:
    print("No English meanings found")

print("Script completed.")
