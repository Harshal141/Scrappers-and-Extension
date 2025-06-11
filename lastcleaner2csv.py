# import json
# import csv

# def cleanDomain(domainName):
#     website = domainName.strip()
#     if website[-1] == "/":
#         website = website[:-1]
#     website = website.replace("http://", "").replace("https://", "").replace("www.", "")
#     website = website.split("/")[0]
#     website = website.lower()
#     return website

# # Load data from JSON file
# input_file = "Injested/2025Feb/luchaCanada/extractedData_parallel.json"
# output_file = "Injested/2025Feb/luchaCanada/extractedData_parallel.csv"


# with open(input_file, "r", encoding="utf-8") as file:
#     data = json.load(file)

# headers = ["name" , "domain"]

# # Open CSV file for writing
# with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
#     writer = csv.writer(csvfile)
    
#     # Write headers
#     writer.writerow(headers)
    
#     # Write data rows
#     for entry in data:
#         name = entry.get("name", "")
#         domain = entry.get("domain", "")

#         if domain is not None:
#             website = cleanDomain(domain)
#         else:
#             continue
        
#         # Write a row to the CSV
#         writer.writerow([name, website])

# print(f"Data successfully saved to {output_file}.")


import csv

# Function to clean domain
def cleanDomain(domainName):
    website = domainName.strip()
    if website[-1] == "/":
        website = website[:-1]
    website = website.replace("http://", "").replace("https://", "").replace("www.", "")
    website = website.split("/")[0]
    website = website.lower()
    return website

# Read the original CSV and process it
input_file = "thomanet_misc.csv"
output_file = "cleaned_domains_thomasnet.csv"

cleaned_data = []

with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        domain = row['domain']
        if domain.strip():  # skip empty domains
            cleaned_domain = cleanDomain(domain)
            cleaned_data.append({'name': row.get('name', ''), 'cleaned_domain': cleaned_domain})

# Write the cleaned data to a new CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = ['name', 'cleaned_domain']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cleaned_data)

print(f"Cleaned domain data saved to {output_file}")
