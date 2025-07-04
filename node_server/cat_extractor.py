import math
import json
import pandas as pd

# Sample of your input category and supplier count (truncated here; assume full list in practice)
categories_and_counts = {
    "Cosmetic Stencils": 8,
    "Manicure Sticks": 12,
    "Sun Care Products": 90,
    "Sunglasses": 192,
    "Sunvisors": 32,
    "Abdominal & Back Supporters": 29,
    "Athletic Supporters": 11,
    "Collar Supporters": 9,
    "Massage Tables": 18,
    "Talcum": 7,
    "Tampons": 36,
    "Hair Setting Tapes": 6,
    "Facial Tissue": 169,
    "Toilet Travel Kits": 31,
    "Toiletries": 116,
    "Toothbrushes": 79,
    "Toothpaste": 78,
    "Toothpicks": 32,
    "Cosmetic Towelettes": 20,
    "Massage Vibrators": 22,
    "Foot Warmers": 23,
    "Wigs, Toupees & Hair Pieces": 18,
}

# Corresponding URLs for each category (sample/truncated for demo)

category_urls = {
    "Cosmetic Stencils": "https://www.thomasnet.com/suppliers/usa/cosmetic-stencils-97008078",
    "Manicure Sticks": "https://www.thomasnet.com/suppliers/usa/manicure-sticks-80500606",
    "Sun Care Products": "https://www.thomasnet.com/suppliers/usa/sun-care-products-81345001",
    "Sunglasses": "https://www.thomasnet.com/suppliers/usa/sunglasses-81346009",
    "Sunvisors": "https://www.thomasnet.com/suppliers/usa/sunvisors-95933818",
    "Abdominal & Back Supporters": "https://www.thomasnet.com/suppliers/usa/abdominal-back-supporters-81353005",
    "Athletic Supporters": "https://www.thomasnet.com/suppliers/usa/athletic-supporters-81353203",
    "Collar Supporters": "https://www.thomasnet.com/suppliers/usa/collar-supporters-81353401",
    "Massage Tables": "https://www.thomasnet.com/suppliers/usa/massage-tables-96076716",
    "Talcum": "https://www.thomasnet.com/suppliers/usa/talcum-82672403",
    "Tampons": "https://www.thomasnet.com/suppliers/usa/tampons-82691403",
    "Hair Setting Tapes": "https://www.thomasnet.com/suppliers/usa/hair-setting-tapes-83625004",
    "Facial Tissue": "https://www.thomasnet.com/suppliers/usa/facial-tissue-85861102",
    "Toilet Travel Kits": "https://www.thomasnet.com/suppliers/usa/toilet-travel-kits-42032003",
    "Toiletries": "https://www.thomasnet.com/suppliers/usa/toiletries-85920205",
    "Toothbrushes": "https://www.thomasnet.com/suppliers/usa/toothbrushes-86570462",
    "Toothpaste": "https://www.thomasnet.com/suppliers/usa/toothpaste-86570504",
    "Toothpicks": "https://www.thomasnet.com/suppliers/usa/toothpicks-86570603",
    "Cosmetic Towelettes": "https://www.thomasnet.com/suppliers/usa/cosmetic-towelettes-96104245",
    "Massage Vibrators": "https://www.thomasnet.com/suppliers/usa/massage-vibrators-91940601",
    "Foot Warmers": "https://www.thomasnet.com/suppliers/usa/foot-warmers-92140201",
    "Wigs, Toupees & Hair Pieces": "https://www.thomasnet.com/suppliers/usa/wigs-toupees-hair-pieces-94054202",
}

# Generate paginated mappings
output = []
index = 1

for category, count in categories_and_counts.items():
    url = category_urls.get(category)
    if not url:
        continue
    base_url = url.split("?")[0]
    for page in range(1, math.ceil(count / 25) + 1):
        paged_url = f"{base_url}?coverage_area=NA&pg={page}"
        output.append({
            "index": index,
            "category": category,
            "url": paged_url
        })
        index += 1

# Save as JSON
json_path = "./thomasnet_category_pages_1.json"
with open(json_path, "w") as f:
    json.dump(output, f, indent=2)
