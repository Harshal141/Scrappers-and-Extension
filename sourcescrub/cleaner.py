import csv

def main():
    first_csv = "test.csv"    # Replace with your first CSV file path
    second_csv = "cleaned_batch_19.csv"  # Replace with your second CSV file path
    output_csv = "cleaned_batch_19_remains.csv"

    # Step 1: Read the first CSV (single column "domain") into a set
    existing_domains = set()
    with open(first_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain_value = row["domain"].strip()
            existing_domains.add(domain_value)

    # Step 2: Read the second CSV (columns "name", "domain")
    filtered_rows = []
    with open(second_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain_value = row["domain"].strip()
            # Step 3: Keep only rows whose domain is NOT in the first CSV's set
            if domain_value not in existing_domains:
                filtered_rows.append(row)

    # Step 4: Write the filtered rows to a new CSV
    # We assume the second CSV's columns are ["name", "domain"]
    with open(output_csv, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "domain"])
        writer.writeheader()
        for row in filtered_rows:
            writer.writerow({"name": row["name"], "domain": row["domain"]})

    print(f"Filtered {len(filtered_rows)} rows. Output saved to {output_csv}")

if __name__ == "__main__":
    main()
