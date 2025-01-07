from bs4 import BeautifulSoup
import requests
import csv

with open('./meatcouncil/source.html') as file:
    soup = BeautifulSoup(file, 'html.parser')

def fetchTitle(website):
    print(f"Fetching title for: {website}")
    try:
        r = requests.get(f"http://{website}", timeout=5)
        r.raise_for_status()  
        tempSoup = BeautifulSoup(r.text, 'html.parser')
        if tempSoup.title:
            return tempSoup.title.string.strip()
        else:
            return "No title found"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {website}: {e}")
        return "Error fetching title"

aTags = soup.find_all('a')

output = []

for aTag in aTags:
    href = aTag.get('href')
    if href:
        website = href.replace("http://", "").replace("https://", "").replace("www.", "")
        website = website.split("/")[0]
        website = website.lower()
        title = fetchTitle(website)
        output.append({
            'website': website,
            'title': title
        })

# Save the output data to a CSV file
csv_file = 'website_titles.csv'

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['website', 'title'])
    writer.writeheader()  # Write the CSV header
    writer.writerows(output)  # Write data rows

print(f"Data saved to {csv_file}")
