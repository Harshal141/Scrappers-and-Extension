from bs4 import BeautifulSoup
from utility import json_to_csv, cleanDomain

with open("./pacGlobal/index.html") as file:
    soup = BeautifulSoup(file, "html.parser")

cellClass = soup.find_all(class_="cell")

data = []

for cell in cellClass:
    domain = cell.find("a")
    if domain:
        website = cleanDomain(domain['href'])
        title = cell.find(class_="bucket-title").text.strip()
        data.append({
            "title": title,
            "domain": website
        })

json_to_csv(data, "output.csv")
