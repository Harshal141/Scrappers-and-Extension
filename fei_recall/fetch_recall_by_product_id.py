import requests
import time
from datetime import datetime
from typing import Union, List, Dict

def sanitize_value(v, max_length=80): #TODO: update the max length check with maya
    try:
        v_str = str(v).replace("\n", " ").replace(",", ";").strip()
        return v_str[:max_length] + "..." if len(v_str) > max_length else v_str
    except Exception:
        return ""
    

def fetch_recall_single(product_id: str) -> dict:
    signature = str(int(datetime.utcnow().timestamp()))
    url = 'https://www.accessdata.fda.gov/rest/iresapi/recalls/?signature=' + signature
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization-User': 'harshal.patil@keychain.com',
        'Authorization-Key': 'Q1J9ollsUmvNyUXa',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    data_template = 'payload={"displaycolumns": "codeinformation,productid,recalleventid,producttypeshort,firmcitynam,firmcountrynam,firmline1adr,firmline2adr,firmpostalcd,phasetxt,recallinitiationdt,firmlegalnam,voluntarytypetxt,distributionareasummarytxt,centercd,firmstateprvncnam,centerclassificationdt,terminationdt,initialfirmnotificationtxt,centerclassificationtypetxt,enforcementreportdt,firmfeinum,firmsurvivingnam,firmsurvivingfei,eventlmd,productdescriptionshort,productshortreasontxt,productdescriptiontxt,recallnum,productdistributedquantity,determinationdt,postedinternetdt","filter":"[{\'productid\':\'product_id\'}]","start":1,"rows": 2,"sort":"productid","sortorder":"asc"}'
    data = data_template.replace("product_id", product_id)

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        time.sleep(1)
        response.raise_for_status()
        json_data = response.json()
        print(f"🔍 Fetched {product_id} from API")
        print(f"Response: {json_data}")

        if json_data.get("MESSAGE") == "success":
            result = json_data.get("RESULT")
            if isinstance(result, list) and result:
                cleaned = {
                    k.lower(): sanitize_value(v)
                    for k, v in result[0].items()
                }
                cleaned["api_status"] = "ok"
                cleaned["product_id"] = product_id
                return cleaned
            else:
                print(f"⚠️ Not found for {product_id}")
                return {"api_status": "not_found", "product_id": product_id}

        else:
            return {"api_status": "error", "product_id": product_id}

    except Exception as e:
        print(f"❌ Error for {product_id}: {e}")
        return {"api_status": "error", "product_id": product_id}

pro_id = "142459"

if __name__ == "__main__":
    result = fetch_recall_single(pro_id)
    print(f"Result for product ID {pro_id}:\n{result}")
    # You can also save this result to a file or database as needed

