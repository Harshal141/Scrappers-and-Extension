# import csv
# import json

# # Input and output file paths
# input_csv_file = "serper/DATA_332/top_manu_1_20.csv"  # Replace with the path to your CSV file
# output_json_file = "serper/DATA_332/top_manu_1_20.json"  # Output JSON file path

# # Read and process the CSV file
# with open(input_csv_file, mode='r' , encoding='utf-8') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     json_output = []
    
#     # Convert rows to indexed JSON format
#     for index, row in enumerate(csv_reader, start=1):
#         json_output.append({
#             "index": index,
#             "name": row.get("name", "").strip() if row.get("name") else "",
#             "url": row.get("domain", "").strip() if row.get("domain") else "",
#         })

# # Write the JSON output to a file
# with open(output_json_file, mode='w') as json_file:
#     json.dump(json_output, json_file, indent=4)

# print(f"JSON file created: {output_json_file}")

import json
import os
from utility import cleanDomain

# File Paths
input_file = "serper/DATA_332/120_/serper_final_filtered.json"
output_file = "serper/DATA_332/120_/serper_final_indexed.json"

# Load JSON Data
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Process Data: Replace 'id' with 'index' and remove duplicates based on 'domain'
processed_data = []
unique_domains = set()

for index, entry in enumerate(data, start=1):  # Iterate over the list
    domain = cleanDomain(entry.get('domain', ''))  # Handle missing 'domain' field

    if not domain:  # Skip entries with an empty domain
        continue

    if domain in unique_domains:
        continue

    processed_data.append({
        'index': index,
        'name': entry.get("name", ""),
        'url': domain
    })
    unique_domains.add(domain)

# Write the processed data to the output file
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, indent=4)

print(f"✅ Processed data successfully saved to {output_file}")
