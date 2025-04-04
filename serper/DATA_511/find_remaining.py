import csv
import json

# Input CSV file path
input_csv = 'top_200_per_name_final.csv'
output_json = 'unique_ingredients.json'

# Use a set to collect unique ingredient names
ingredients_set = set()
domain_set = set()

with open(input_csv, mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:  # Skip empty rows
            ingredient = row[0].strip()
            domain = row[1].strip()
            if domain: 
                domain_set.add(domain)
            if ingredient:  
                ingredients_set.add(ingredient)

# Convert to sorted list (optional)
unique_ingredients = sorted(ingredients_set)

# Write to JSON file
with open(output_json, 'w', encoding='utf-8') as jsonfile:
    json.dump(unique_ingredients, jsonfile, indent=4)

print(f"Extracted {len(unique_ingredients)} unique ingredients to {output_json}")
print(f"Extracted {len(domain_set)} unique domains")