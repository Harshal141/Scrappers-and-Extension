import json

def process_json(input_file, output_file):
    # Read the JSON data from the input file
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Use a dictionary to remove duplicates based on the 'name' field
    unique_data = {}
    for entry in data:
        if entry['name'] not in unique_data:
            unique_data[entry['name']] = entry

    # Replace 'id' with 'index' and create a list of unique entries
    processed_data = []
    for index, (name, entry) in enumerate(unique_data.items(), start=1):
        processed_data.append({
            'index': index,
            'name': entry['name'],
            'url': entry['domain']
        })

    # Write the processed data to the output file
    with open(output_file, 'w') as file:
        json.dump(processed_data, file, indent=4)

# Example usage
input_file = './dnb/DNB_list.json'
output_file = './dnb/DNB_filtered.json'  
process_json(input_file, output_file)