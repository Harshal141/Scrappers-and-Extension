# #import required libraries
# import requests
# import json
# import datetime

# #create a signature and append it to the URL to avoid cached responses from server.
# signature = str(int(datetime.datetime.now().timestamp()))

# #set the url 
# url = 'https://www.accessdata.fda.gov/rest/iresapi/recalls/?signature='+signature

# #set headers
# headers = {
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Authorization-User': 'harshal.patil@keychain.com',
#     'Authorization-Key': 'Q1J9ollsUmvNyUXa',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
# }

# # get initial response to fetch RESULTCOUNT
# data_template = 'payload={"displaycolumns": "productid,recalleventid,producttypeshort,firmcitynam,firmcountrynam,firmline1adr,firmline2adr,firmpostalcd,phasetxt,recallinitiationdt,firmlegalnam,voluntarytypetxt,distributionareasummarytxt,centercd,firmstateprvncnam,centerclassificationdt,terminationdt,initialfirmnotificationtxt,centerclassificationtypetxt,enforcementreportdt,firmfeinum,firmsurvivingnam,firmsurvivingfei,eventlmd,productdescriptiontxt,productshortreasontxt,recallnum,productdistributedquantity,determinationdt,postedinternetdt","filter":"[{\'eventlmdfrom\':\'07/24/2018\'},{\'eventlmdto\':\'09/24/2021\'},{\'centerclassificationtypetxt\':[\'3\',\'2\',\'1\',\'NC\']},{\'centercd\':[\'CBER\',\'CFSAN\']}]","start":%d,"rows": 20,"sort":"productid","sortorder":"asc"}'

# start = 1
# rows = 20
# max_pages = 100  # limit to 100 pages
# current_page = 0
# all_records = []

# while current_page < max_pages:
#     data = data_template % start
#     response = requests.post(url, headers=headers, data=data)
#     json_result = response.json()
    
#     if 'RESULT' not in json_result or not json_result['RESULT']:
#         break
    
#     result = json_result.get('RESULT')
#     print(f"Fetching records from start={start}, got {len(result)} records.")
    
#     all_records.extend(result)  # store full record instead of just productid
    
#     start += rows
#     current_page += 1

#     if current_page == 1:
#         total_records = json_result.get('RESULTCOUNT', 0)
#         print(f"Total expected records: {total_records}")
#         print(f"Limiting to first {max_pages} pages ({rows * max_pages} records max).")

# # Save to JSON file
# with open("fda_recall_records_first_100_pages.json", "w") as f:
#     json.dump(all_records, f, indent=2)

# print(f"Done. Total records saved: {len(all_records)}")



#import required libraries
import requests
import json
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

#create a signature and append it to the URL to avoid cached responses from server.
signature = str(int(datetime.datetime.now().timestamp()))

#set the url 
url = 'https://www.accessdata.fda.gov/rest/iresapi/recalls/?signature=' + signature

#set headers
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization-User': 'harshal.patil@keychain.com',
    'Authorization-Key': 'Q1J9ollsUmvNyUXa',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# fixed payload template
data_template = 'payload={"displaycolumns": "codeinformation,productid,recalleventid,producttypeshort,firmcitynam,firmcountrynam,firmline1adr,firmline2adr,firmpostalcd,phasetxt,recallinitiationdt,firmlegalnam,voluntarytypetxt,distributionareasummarytxt,centercd,firmstateprvncnam,centerclassificationdt,terminationdt,initialfirmnotificationtxt,centerclassificationtypetxt,enforcementreportdt,firmfeinum,firmsurvivingnam,firmsurvivingfei,eventlmd,productdescriptiontxt,productshortreasontxt,recallnum,productdistributedquantity,determinationdt,postedinternetdt","filter":"[{\'productid\':\'203305\'}]","start":1,"rows": 2,"sort":"productid","sortorder":"asc"}'

# settings
rows = 20
max_pages = 1
concurrent_threads = 10

# function to fetch a single page
def fetch_page(start):
    data = data_template
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        json_result = response.json()
        result = json_result.get('RESULT', [])
        print(f"Thread: start={start}, fetched {len(result)} records.")
        return result
    except Exception as e:
        print(f"Error on start={start}: {e}")
        return []

# build all start values
start_offsets = [1 + i * rows for i in range(max_pages)]

# parallel fetch
all_records = []
with ThreadPoolExecutor(max_workers=concurrent_threads) as executor:
    future_to_start = {executor.submit(fetch_page, start): start for start in start_offsets}
    for future in as_completed(future_to_start):
        records = future.result()
        all_records.extend(records)

# save to JSON
with open("fda_recall_records_first_100_pages.json", "w") as f:
    json.dump(all_records, f, indent=2)

print(f"Done. Total records saved: {len(all_records)}")


