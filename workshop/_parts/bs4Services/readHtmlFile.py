from bs4 import BeautifulSoup

INPUT_FILE = 'workshop/usdairy/index.html'

with open(INPUT_FILE) as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
