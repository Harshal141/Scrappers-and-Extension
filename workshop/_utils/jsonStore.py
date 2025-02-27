import json

# Function to append data to JSON file in a thread-safe manner
def appendJsonDataToFile(new_data, OUTPUT_JSON):
    try:
        with open(OUTPUT_JSON, 'r') as f:
            existing = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []

    existing.extend(new_data)

    with open(OUTPUT_JSON, 'w') as f:
        json.dump(existing, f, indent=4)