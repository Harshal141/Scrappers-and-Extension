# get unique names form data.json
import json

with open("expowest/data.json", "r") as file:
    data = json.load(file)

newData = []

names = set()
for item in data:
    if item["name"] not in names:
        names.add(item["name"])
        newData.append(item)
    
print(len(names), "unique names found")

with open("expowest/unique_data.json", "w") as file:
    json.dump(newData, file, indent=4)
