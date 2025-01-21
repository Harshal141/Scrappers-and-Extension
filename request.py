import pandas as pd
import json
from utility import cleanDomain

# Input and output file paths
input_csv_file = "./thomas/DATA_297_thomas_packaging_2.csv"  # Replace with your input CSV file name
output_json_file = "output.json"  # Replace with your desired output JSON file name

# Read the CSV data from the file
df = pd.read_csv(input_csv_file)

# Drop rows with NaN in the 'domain' column
df = df.dropna(subset=['domain'])

# Apply the cleanDomain function to the 'domain' column and ensure uniqueness
df['domain'] = df['domain'].apply(cleanDomain)
df = df.drop_duplicates(subset=['domain'])

# Add an index column starting from 1
df.reset_index(drop=True, inplace=True)
df['index'] = df.index + 1

# Rename columns to match the JSON structure
df.rename(columns={'name': 'name', 'domain': 'url'}, inplace=True)

# Convert DataFrame to a list of dictionaries
json_data = df.to_dict(orient='records')

# Write the JSON output to a file
with open(output_json_file, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print(f"JSON data has been written to {output_json_file}")
