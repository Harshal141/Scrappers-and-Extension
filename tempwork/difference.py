import pandas as pd

def filter_domains(csv1_path, csv2_path, output_csv_path):
    # Load the first CSV (list of domains)
    df1 = pd.read_csv(csv1_path)
    
    # Load the second CSV (name, domain mapping)
    df2 = pd.read_csv(csv2_path)
    
    # Ensure both dataframes have the domain column
    df1.columns = ["domain"]
    df2.columns = ["name", "domain"]
    
    # Convert domain column to lowercase to ensure case-insensitive matching
    df1["domain"] = df1["domain"].str.lower()
    df2["domain"] = df2["domain"].str.lower()
    
    # Filter domains that are in df1 but not in df2
    filtered_domains = df2[~df2["domain"].isin(df1["domain"])]
    
    # Save the result to a new CSV
    filtered_domains.to_csv(output_csv_path, index=False)
    print(f"Filtered CSV saved to {output_csv_path}")

if __name__ == "__main__":
    csv1_path = "maindata.csv"  # Update with actual path
    csv2_path = "0sourcescrub-batch-6.csv"  # Update with actual path
    output_csv_path = "difference.csv"  # Update with actual path
    
    filter_domains(csv1_path, csv2_path, output_csv_path)
