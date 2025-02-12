store = [
    {
        "site": "https://www.thomasnet.com/suppliers/search?cov=NA&heading=97009673&searchsource=suppliers&searchterm=sweeten&what=Sweeteners&coverage_area=NA&pg=",
        "maxPage": 6
    },
    {
        "site": "https://www.thomasnet.com/suppliers/search?cov=NA&heading=62760608&searchsource=suppliers&searchterm=preser&what=Preservatives&coverage_area=NA&pg=",
        "maxPage": 7
    },
    {
        "site": "https://www.thomasnet.com/suppliers/search?cov=NA&heading=16493009&searchsource=suppliers&searchterm=food+colo&what=Food+Colors&coverage_area=NA&pg=",
        "maxPage": 2
    },
    {
        "site": "https://www.thomasnet.com/suppliers/search?cov=NA&heading=85371003&searchsource=suppliers&searchterm=thickener&what=Thickeners&coverage_area=NA&pg=",
        "maxPage": 6
    },
    {
        "site": "https://www.thomasnet.com/suppliers/search?cov=NA&heading=581272&searchsource=suppliers&searchterm=emul&what=Emulsifying+Agents&coverage_area=NA&pg=",
        "maxPage": 4
    },
    {
        "site": "https://www.thomasnet.com/suppliers/search?cov=NA&format=json&heading=208009&limit=15&searchsource=suppliers&searchterm=Acid&what=Acid&which=prod&coverage_area=NA&pg=",
        "maxPage": 22
    },
    {
        "site": "https://www.thomasnet.com/suppliers/search?cov=NA&heading=95999926&searchsource=suppliers&searchterm=salt&what=Salts&coverage_area=NA&pg=",
        "maxPage": 9
    },
    {
        "site": "https://www.thomasnet.com/suppliers/search?cov=NA&heading=30331102&searchsource=suppliers&searchterm=flavor&what=Flavorings+&+Flavors=&coverage_area=NA&pg=",
        "maxPage": 10
    }
]

import json

# Generate formatted JSON
output_json = []
index = 1  # Start indexing from 1

for entry in store:
    base_url = entry["site"]
    max_page = entry["maxPage"]
    
    for page in range(1, max_page + 1):
        output_json.append({
            "index": index,
            "name": f"l{index}",
            "url": f"{base_url}{page}"
        })
        index += 1

# Print the output JSON
print(json.dumps(output_json, indent=4))

with open("injested/thomas/DATA_385/index.json", "w") as file:
    json.dump(output_json, file, indent=4)