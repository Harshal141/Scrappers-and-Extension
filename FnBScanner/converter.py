import json
import csv

# Input file containing JSON data
input_file = "./FnBScanner/FnBResult.json"  # Replace with the name of your file
output_file = "./FnBScanner/FnBResult_Jan_2025.csv"

# Load JSON data from the file
with open(input_file, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Extract relevant fields
fields = ['manufacturer_id', 'isRelated']

# Write the extracted data to a CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for item in json_data:
        writer.writerow({field: item.get(field) for field in fields})

print(f"CSV file '{output_file}' created successfully.")
