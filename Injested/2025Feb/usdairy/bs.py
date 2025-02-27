from bs4 import BeautifulSoup

with open('workshop/usdairy/index.html') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# get all last two digits of hrefs

# get all hrefs
hrefs = soup.find_all('a')
for href in hrefs:
    print(href['href'][-2:])
