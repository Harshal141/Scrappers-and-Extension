import json
import csv

def json_to_csv(json_file, csv_file):
    # Read JSON data from the file
    with open(json_file, 'r', encoding='utf-8') as jf:
        data = json.load(jf)

    # Open CSV file for writing
    with open(csv_file, 'w', newline='', encoding='utf-8') as cf:
        writer = csv.writer(cf)
        # Write CSV header
        writer.writerow(["name", "website"])
        # Write each JSON object as a CSV row
        for item in data:
            writer.writerow([item.get("website", "")])

if __name__ == '__main__':
    json_input_file = 'total_ift.json'     # Replace with your JSON file path
    csv_output_file = 'output.csv'      # Replace with your desired CSV file path
    json_to_csv(json_input_file, csv_output_file)
    print(f"CSV file has been written to {csv_output_file}")
