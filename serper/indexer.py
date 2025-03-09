import csv
import json

def csv_to_json(csv_path, json_path):
    data = []
    
    with open(csv_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)  # Read the first row as headers
        
        for index, row in enumerate(csv_reader, start=1):
            entry = {
                "index": index,
                "name": row[0],
            }
            data.append(entry)
    
    json_output = {"packaging_data": data}
    
    with open(json_path, mode='w', encoding='utf-8') as json_file:
        json.dump(json_output, json_file, indent=2)
    
    print(f"JSON file saved at: {json_path}")

# Example usage:
csv_path = "workshop/fssc/usa.csv"  # Change this to your CSV file path
json_path = "workshop/fssc/usa.csv"  # Change this to desired JSON output path
csv_to_json(csv_path, json_path)

# make csv have unique domain names
# import csv

# with open('serper/DATA_332/comb_1_40_ai.csv', mode='r', encoding='utf-8') as csv_file:
#     csv_reader = csv.reader(csv_file)
#     headers = next(csv_reader)
#     domain_names = set()
#     unique_rows = []
#     for row in csv_reader:
#         if row[1] not in domain_names:
#             domain_names.add(row[1])
#             unique_rows.append(row)

# with open('serper/DATA_332/comb_1_40_ai_unique.csv', mode='w', encoding='utf-8', newline='') as csv_file:
#     csv_writer = csv.writer(csv_file)
#     csv_writer.writerow(headers)
#     csv_writer.writerows(unique_rows)

# print("Unique CSV file created successfully.")







# import json 

# with open("serper/DATA_332/120_/serper_final.json", mode='r', encoding='utf-8') as json_file:
#     data = json.load(json_file)
#     print(data[0])

# # unique domain names

# new_data = []
# unique_domain_names = set()
# for row in data:
#     if row['domain'] not in unique_domain_names:
#         unique_domain_names.add(row['domain'])
#         new_data.append(row)

# with open("serper/DATA_332/120_/serper_final_unique.json", mode='w', encoding='utf-8') as json_file:
#     json.dump(new_data, json_file, indent=2)








# import json

# def remove_common_entries(small_file, big_file, output_file):
#     # Load small JSON file
#     with open(small_file, 'r', encoding='utf-8') as f:
#         small_data = json.load(f)
    
#     # Load big JSON file
#     with open(big_file, 'r', encoding='utf-8') as f:
#         big_data = json.load(f)
    
#     # Extract domains from small file
#     small_domains = {entry['domain'] for entry in small_data}
    
#     # Filter big data to remove entries with matching domains
#     filtered_big_data = [entry for entry in big_data if entry['domain'] not in small_domains]
    
#     # Save the filtered data to a new JSON file
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(filtered_big_data, f, indent=2)
    
#     print(f"Filtered JSON saved to {output_file}")

# # Example usage
# small_json_file = "serper/DATA_332/41_80/serper_41_80_unique.json"
# big_json_file = "serper/DATA_332/120_/serper_final_filtered.json"
# output_json_file = "serper/DATA_332/120_/serper_final_filtered_temp.json"
# remove_common_entries(small_json_file, big_json_file, output_json_file)
