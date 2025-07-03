import requests

AUTH_USER = "harshal.patil@keychain.com"
AUTH_KEY = "Q1J9ollsUmvNyUXa"
BASE_URL = "https://www.accessdata.fda.gov/rest/iresapi/recalls/product"

def fetch_recall_by_product_id_parsed(product_id: int) -> list[dict]:
    url = f"{BASE_URL}/{product_id}"
    headers = {
        "Authorization-User": AUTH_USER,
        "Authorization-Key": AUTH_KEY,
        "User-Agent": "FDA Recall Bot (Python)",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        print(f"✅ Status: {data.get('MESSAGE')} | Count: {data.get('RESULTCOUNT')}")

        # Convert COLUMNS + DATA into list of dictionaries
        columns = data.get("RESULT", {}).get("COLUMNS", [])
        values_list = data.get("RESULT", {}).get("DATA", [])
        parsed_records = [dict(zip(columns, values)) for values in values_list]

        return parsed_records

    except Exception as e:
        print(f"❌ Failed to fetch data for product ID {product_id}: {e}")
        return []

# 🔍 Example usage
product_id = 142459
records = fetch_recall_by_product_id_parsed(product_id)

if records:
    from pprint import pprint
    pprint(records[0])  # Show first recall record
