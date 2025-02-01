from bs4 import BeautifulSoup
import json

# Open and read the index.html file
with open("./unpa/index.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Find all member sections
members = soup.find_all("div", class_="members-section")

# Extract names and URLs
data = []
for member in members:
    name_tag = member.find("div", class_="members-title")
    url_tag = member.find("a", class_="members-urlAdd")

    name = name_tag.text.strip() if name_tag else "No Name Found"
    url = url_tag["href"] if url_tag else "No URL Found"

    print(f"Name: {name}\nURL: {url}\n")
    data.append({"name": name, "url" : url})

with open("./unpa/output.json", 'w') as f:
    json.dump(data, f, indent=4)

