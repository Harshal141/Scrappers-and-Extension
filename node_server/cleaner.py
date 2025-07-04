import json
import pandas as pd

# File paths
input_json_path = "node_server/data_cat2_f.json"
output_csv_path = "node_server/data_cat2_cleaned.csv"

# Domain cleaning function
def cleanDomain(domainName):
    website = domainName.strip()
    if not website or website == "Domain not found!":
        return None
    if website.endswith("/"):
        website = website[:-1]
    website = website.replace("http://", "").replace("https://", "").replace("www.", "")
    website = website.split("/")[0]
    return website.lower()

# Read JSON
with open(input_json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Clean, filter, and deduplicate domains
seen_domains = set()
cleaned_data = []

for entry in data:
    name = entry.get("name", "").strip()
    domain = entry.get("domain", "").strip()
    cleaned_domain = cleanDomain(domain)
    if cleaned_domain and cleaned_domain not in seen_domains:
        cleaned_data.append({"name": name, "domain": cleaned_domain})
        seen_domains.add(cleaned_domain)

# Save to CSV
df = pd.DataFrame(cleaned_data)
df.to_csv(output_csv_path, index=False)
