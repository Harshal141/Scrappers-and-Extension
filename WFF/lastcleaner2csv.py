import json
import csv

def cleanDomain(domainName):
    website = domainName.strip()
    if website[-1] == "/":
        website = website[:-1]
    website = website.replace("http://", "").replace("https://", "").replace("www.", "")
    website = website.split("/")[0]
    website = website.lower()
    return website

# Load data from JSON file
input_file = "./WFF/extracted_data.json"
with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Prepare CSV output
output_file = "./WFF/extracted_data.csv"

# Define CSV headers
headers = ["name" , "Domain"]


# Open CSV file for writing
with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    
    # Write headers
    writer.writerow(headers)
    
    # Write data rows
    for entry in data:
        name = entry.get("name", "")
        domain = entry.get("domain", "")

        if domain is not None:
            website = cleanDomain(domain)
        else:
            continue
        
        # Write a row to the CSV
        writer.writerow([name, website])

print(f"Data successfully saved to {output_file}.")
