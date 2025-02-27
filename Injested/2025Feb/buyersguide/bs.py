import requests
from bs4 import BeautifulSoup
import string
import pandas as pd

# Headers copied from the curl command
headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.nutraceuticalsworld.com',
    'Referer': 'https://www.nutraceuticalsworld.com/buyersguide/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

# URL from curl
url = 'https://www.nutraceuticalsworld.com/wp-admin/admin-ajax.php'

# Store extracted data
results = []

# Iterate through letters A-Z
for letter in string.ascii_uppercase:
    data = {
        'action': 'filter_posts_by_title_first_letter',
        'firstLatter': letter,
        'c_cat': '',
        'country': '',
        'state': ''
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        for link in links:
            href = link.get('href')
            text = link.text.strip()
            if href:
                results.append({'Letter': letter, 'Text': text, 'URL': href})
        print(f"[✅] Processed letter: {letter}")
    else:
        print(f"[❌] Failed for letter {letter} with status code: {response.status_code}")

# Convert results to DataFrame and display to user
df = pd.DataFrame(results)

# Optionally save to CSV
df.to_csv('extracted_urls.csv', index=False)
print("✅ Data saved to 'extracted_urls.csv'")
