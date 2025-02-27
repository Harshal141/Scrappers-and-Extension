import json

# Input and Output Files
input_file = 'companies.json'
output_file = 'filtered.json'

# Location keywords to filter out
exclude_locations = ['usa', 'united states', 'canada']

def filter_locations(file_path):
    """
    Filters out entries where location is USA or Canada.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Filter data
    filtered_data = [
        entry for entry in data
        if entry.get('location', '').lower() in exclude_locations
    ]

    # Save filtered data to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=4)

    print(f"Filtered data saved to {output_file}")
    print(f"{len(filtered_data)} entries kept after filtering.")

if __name__ == '__main__':
    filter_locations(input_file)
