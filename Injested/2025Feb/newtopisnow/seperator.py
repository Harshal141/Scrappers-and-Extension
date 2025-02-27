import json 

from utility import cleanDomain

with open("workshop/newtopisnow/output.json", "r") as f:
    data = json.load(f)

cleanedPath = "workshop/newtopisnow/cleaned.json"
serperPath = "workshop/newtopisnow/seperated.json"

cleanedData = []
serperatedData = []

for item in data:
    if item['url'] == '':
        serperatedData.append(item)
    else:
        item['url'] = cleanDomain(item['url'])
        cleanedData.append(item)

with open(cleanedPath, "w") as f:
    json.dump(cleanedData, f, indent=4)

with open(serperPath, "w") as f:
    json.dump(serperatedData, f, indent=4)