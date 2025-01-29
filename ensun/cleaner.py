import json
from utility import cleanDomain

data = []
with open("./ensun/company_data.json", "r") as json_file:
    data = json.load(json_file)

print(f"Total companies scraped: {len(data)}")

newJson = []

unique_urls = set()
for company in data:
    cleanedUrl = cleanDomain(company["url"])
    if cleanedUrl not in unique_urls:
        unique_urls.add(cleanedUrl)
        newJson.append(company)

with open("./ensun/DATA_319_cleaned_data.json", "w") as json_file:
    json.dump(newJson, json_file, indent=4)
