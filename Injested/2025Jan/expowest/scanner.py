from bs4 import BeautifulSoup
import json
import re


def clean_text(text):

    if not text:
        return ""
    
    # Replace newlines and tabs with a space
    text = re.sub(r'[\n\r\t]+', ' ', text)

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    # Strip leading/trailing spaces
    return text.strip()

# Base URL to complete relative links
base_url = 'https://www.expowest.com/'

# Load the HTML file
with open('./expowest/index.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, "html.parser")

data = []

# Loop through all anchor (<a>) tags
for a in soup.find_all('a'):
    url = a.get('href')
    
    # Skip absolute URLs (external links)
    if url and url.startswith('http'):
        continue
    
    # Construct full URL
    url = base_url + url if url else base_url

    # Extract the <span> inside <a> and clean the text
    span = a.find('span', class_='sc-a13c392f-0 sc-5729954b-3 ffVsRx csdXSf')
    
    if span:
        name = clean_text(span.get_text())
        data.append({"name": name, "url": url})

# Save the cleaned data to a JSON file
with open('./expowest/data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print("✅ Data saved to expowest/data.json")
