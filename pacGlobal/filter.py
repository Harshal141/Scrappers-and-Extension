from bs4 import BeautifulSoup
import csv

# Parse the HTML file with BeautifulSoup
with open("./pacGlobal/index.html") as file:
    soup = BeautifulSoup(file, "html.parser")

cellClass = soup.find_all(class_="cell")

data = []

for cell in cellClass:
    # Get the <a> tag href
    domain = cell.find("a")
    if domain:
        website = domain['href'].strip()
        if website[-1] == "/":
            website = website[:-1]
        website = website.replace("http://", "").replace("https://", "").replace("www.", "")
        website = website.split("/")[0]
        website = website.lower()
        title = cell.find(class_="bucket-title").text.strip()
        data.append({
            "title": title,
            "domain": website
        })

with open("./pacGlobal/pacGlobal.csv", "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ["title", "domain"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data)

print("Data has been saved to output.csv!")
