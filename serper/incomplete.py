import json

def check_domains_in_json(file_path, output_file):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return [], []
    
    names_missing_domains = []
    names_with_200_domains = []
    
    for name, domains in data.items():
        if len(domains) < 100:
            names_missing_domains.append(name)
            print(f"{name} has only {len(domains)} domains.")
        else:
            names_with_200_domains.append(name)
    
    if not names_missing_domains:
        print("All names have 200 or more domains.")
    else:
        print(f"{len(names_missing_domains)} names are missing domains.")
    
    print("List of names with 200 domains:")
    print(names_with_200_domains)
    
    # Save names with 200 domains to a file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(names_with_200_domains, f, indent=4)
        print(f"Saved names with 200 domains to {output_file}")
    except Exception as e:
        print(f"Error saving file {output_file}: {e}")
    
    return names_missing_domains, names_with_200_domains

if __name__ == "__main__":
    json_file = "DATA_511/top_200_per_name1.json"  
    output_file = "DATA_511/names_with_200_domains.json"
    missing_names, complete_names = check_domains_in_json(json_file, output_file)
    
    if missing_names:
        print("Names that need to be re-run:", missing_names)
    
    if complete_names:
        print("Names with 200 domains saved in:", output_file)