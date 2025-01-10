from bs4 import BeautifulSoup
from utility import json_to_csv, cleanDomain

with open("./fhcp/index.html") as file:
    soup = BeautifulSoup(file, "html.parser")

memberClass = soup.find_all(class_="memberListingOuter")

data = []

for member in memberClass:
    name = member.find_all(class_="text-center")[1].text.strip()
    domain = member.find("a")["href"]
    website = cleanDomain(domain)
    data.append({
        "name": name,
        "domain": website
    })

json_to_csv(data, "output.csv")


