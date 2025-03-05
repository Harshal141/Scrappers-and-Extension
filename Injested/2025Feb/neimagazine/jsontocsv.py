import json
import csv

# Input and Output Files
input_file = 'neimaganzine_final.json'
output_file = 'neimaganzine_final.csv'

def json_to_csv(file_path):
    """
    Converts JSON data to a CSV file with Name (empty) and Domain columns.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Open CSV for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Name', 'Domain'])
        
        # Write rows with Name as empty and Domain from JSON
        for entry in data:
            domain = entry.get('domain', '')
            writer.writerow(['', domain])  # Name is empty

    print(f"CSV file '{output_file}' created successfully.")

if __name__ == '__main__':
    json_to_csv(input_file)
