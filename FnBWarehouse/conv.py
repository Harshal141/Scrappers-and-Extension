# import csv
# import json

# # Input and output file paths
# input_csv_file = "./FnBWarehouse/pacGlobal.csv"  # Replace with the path to your CSV file
# output_json_file = "./FnBWarehouse/indexed_pacGlobal.json"  # Output JSON file path

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

input_file = "output.json"
output_file ="source.json"

with open(input_file, 'r') as file:
    data = json.load(file)

# Use a dictionary to remove duplicates based on the 'name' field
unique_data = {}
for entry in data:
    if entry['name'] not in unique_data:
        unique_data[entry['name']] = entry

# Replace 'id' with 'index' and create a list of unique entries
processed_data = []
unique_domain = set()
for index, (name, entry) in enumerate(unique_data.items(), start=1):
    domain = cleanDomain(entry['url'])
    if domain in unique_domain:
        continue
    processed_data.append({
        'index': index,
        'name': entry['name'],
        'url': domain
    })
    unique_domain.add(domain)

# Write the processed data to the output file
with open(output_file, 'w') as file:
    json.dump(processed_data, file, indent=4)