import json
import csv

# Input and Output Files
input_file = 'filtered.json'
output_file = 'filtered.csv'

def json_to_csv(file_path):
    """
    Converts JSON data to a CSV file with Name and Domain columns.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Open CSV for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Domain'])
        
        # Write rows
        for entry in data:
            name = entry.get('name', 'N/A')
            domain = entry.get('domain', 'N/A')
            writer.writerow([domain])

    print(f"CSV file '{output_file}' created successfully.")

if __name__ == '__main__':
    json_to_csv(input_file)
