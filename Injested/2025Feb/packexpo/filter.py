import json
import re

# Input and Output Files
input_file = 'output.json'
output_file = 'filtered_us_ca_packExpo.json'

# List of USA State Abbreviations and Full Names
usa_states = [
    "al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga", "hi", "id", "il", "in", "ia", 
    "ks", "ky", "la", "me", "md", "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh", "nj", 
    "nm", "ny", "nc", "nd", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "vt", 
    "va", "wa", "wv", "wi", "wy",
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", 
    "delaware", "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", 
    "kansas", "kentucky", "louisiana", "maine", "maryland", "massachusetts", "michigan", 
    "minnesota", "mississippi", "missouri", "montana", "nebraska", "nevada", "new hampshire", 
    "new jersey", "new mexico", "new york", "north carolina", "north dakota", "ohio", 
    "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina", "south dakota", 
    "tennessee", "texas", "utah", "vermont", "virginia", "washington", "west virginia", 
    "wisconsin", "wyoming"
]

# List of Canadian Provinces Abbreviations and Full Names
canada_provinces = [
    "ab", "bc", "mb", "nb", "nl", "ns", "nt", "nu", "on", "pe", "qc", "sk", "yt",
    "alberta", "british columbia", "manitoba", "new brunswick", "newfoundland and labrador", 
    "nova scotia", "nunavut", "ontario", "prince edward island", "quebec", "saskatchewan", 
    "yukon"
]

# Keywords for country names
usa_keywords = ['united states', 'usa', 'united states of america']
canada_keywords = ['canada']

def is_usa_or_canada(address):
    """
    Checks if the address is in USA or Canada.
    """
    address = address.lower()

    # Check for country names
    if any(keyword in address for keyword in usa_keywords + canada_keywords):
        return True

    # Check for USA state abbreviations or full state names
    if any(re.search(r'\b' + state + r'\b', address) for state in usa_states):
        return True

    # Check for Canadian province abbreviations or full names
    if any(re.search(r'\b' + province + r'\b', address) for province in canada_provinces):
        return True

    return False

def filter_addresses(file_path):
    """
    Filters addresses from the JSON file for entries in USA or Canada.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Filter data
    filtered_data = []
    for entry in data:
        address = entry.get('address', '')
        if is_usa_or_canada(address):
            filtered_data.append(entry)

    # Save filtered data to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=4)

    print(f"Filtered data saved to {output_file}")
    print(f"{len(filtered_data)} entries found for USA or Canada.")

if __name__ == '__main__':
    filter_addresses(input_file)
