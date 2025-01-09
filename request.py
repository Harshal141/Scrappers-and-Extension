import csv
import json

def csv_to_json_with_index(csv_file, json_file):
    data = []
    
    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for idx, row in enumerate(csv_reader, start=1):
            indexed_row = {"index": idx, **row}
            data.append(indexed_row)
    
    with open(json_file, mode='w') as file:
        json.dump(data, file, indent=4)

# Input and output file paths
csv_file = 'source.csv'  # Replace with your CSV file path
json_file = 'output.json'  # Replace with your desired JSON output file path

csv_to_json_with_index(csv_file, json_file)
