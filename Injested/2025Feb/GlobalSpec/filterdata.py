import json

def main():
    # Load headquarters list from headquater.json
    with open("us_canada_headquarters.json", "r", encoding="utf-8") as f:
        headquarters_list = json.load(f)
    
    # Normalize headquarters strings (strip extra spaces)
    headquarters_set = set(hq.strip() for hq in headquarters_list)
    
    # Load supplier data from final_supplier.json
    with open("final_supplier.json", "r", encoding="utf-8") as f:
        suppliers = json.load(f)
    
    # Filter supplier entries whose supplier_HeadQuarter is in the headquarters_set
    filtered_suppliers = []
    for supplier in suppliers:
        supplier_hq = supplier.get("supplier_HeadQuarter", "").strip()
        if supplier_hq in headquarters_set:
            filtered_suppliers.append(supplier)
    
    # Remove duplicate supplier entries.
    # We use a tuple of (supplier_name, supplier_website) as the unique key.
    unique_suppliers = {}
    for sup in filtered_suppliers:
        key = (sup.get("supplier_name", "").strip(), sup.get("supplier_website", "").strip())
        unique_suppliers[key] = sup  # This will overwrite duplicates
    
    final_filtered = list(unique_suppliers.values())
    
    # Write the final unique, filtered supplier data to final_filteredData.json
    output_file = "final_filteredData.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_filtered, f, indent=4)
    
    print(f"Final filtered data contains {len(final_filtered)} unique supplier(s).")
    
if __name__ == "__main__":
    main()
