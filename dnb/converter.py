def cleanDomain(domainName):
    website = domainName.strip()
    if website[-1] == "/":
        website = website[:-1]
    website = website.replace("http://", "").replace("https://", "").replace("www.", "")
    website = website.split("/")[0]
    website = website.lower()
    return website

import csv
import json
from typing import List, Dict, Any

def flatten_json(nested_json: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """
    Flattens a nested JSON object into a single-level dictionary with dot-separated keys.

    Args:
        nested_json (dict): The JSON object to flatten.
        parent_key (str): The base key for recursion.
        sep (str): Separator for nested keys.

    Returns:
        dict: A flattened dictionary.
    """
    items = []
    for k, v in nested_json.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for idx, item in enumerate(v):
                items.extend(flatten_json({f"{new_key}[{idx}]": item}).items())
        else:
            items.append((new_key, v))
    return dict(items)

def json_to_csv(json_data: List[Dict[str, Any]], output_file: str) -> None:
    """
    Converts a JSON array to a CSV file.

    Args:
        json_data (list): List of JSON objects to convert.
        output_file (str): Path of the CSV file to create.
    """
    # Flatten the JSON objects
    flattened_data = [flatten_json(item) for item in json_data]

    # Extract CSV headers from flattened JSON keys
    headers = set()
    for item in flattened_data:
        headers.update(item.keys())
    headers = sorted(headers)

    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(flattened_data)

    print(f"CSV file '{output_file}' created successfully.")

with open("./dnb/datacanada.json", "r", encoding="utf-8") as file:
    data = json.load(file)

filtered_data = [
    {**item, "domain": cleanDomain(item["domain"])}
    for item in data
    if "domain" in item
]

json_to_csv(filtered_data, "./dnb/datacanada.csv")