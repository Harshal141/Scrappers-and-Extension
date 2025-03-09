import csv
import json

# Input and Output Files
input_file = 'AmericanFrozen.csv'
output_file = 'AmericanFrozen.json'

def csv_to_json(file_path):
    """
    Converts a CSV file containing company names to JSON format.
    """
    data = []

    # Open CSV for reading
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Extract each name and store it in a dictionary
        for row in reader:
            name = row.get('Name', '').strip()
            if name:  # Only add non-empty names
                data.append({"name": name})

    # Save the result to a JSON file
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

    print(f"JSON file '{output_file}' created successfully.")

if __name__ == '__main__':
    csv_to_json(input_file)
