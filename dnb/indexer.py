import json

def add_index_to_json(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    # Add an index to each item in the list
    for i, item in enumerate(data):
        item["index"] = i + 1  # Index starting from 1 (or use `i` for 0-based indexing)

    # Save the updated data back to the file
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Index added to {len(data)} items in {json_file_path}")

add_index_to_json("./dnb/company_data.json")