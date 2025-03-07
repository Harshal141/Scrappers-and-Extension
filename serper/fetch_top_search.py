import requests
import logging
from dotenv import load_dotenv
import csv
import json
import os
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


load_dotenv()

SERPER_API_KEY = os.getenv('SERPER_API_KEY_V2')
SERPER_API_URL = 'https://google.serper.dev/search'

INPUT_JSON_FILE = "DATA_511/ingridients_source.json"
OUTPUT_JSON_FILE = "DATA_511/top_200_per_name1.json"
OUTPUT_CSV_FILE = "DATA_511/top_200_per_name1.csv"
LOG_FILE = "fetch_log.log"
COMPLETED_PACKAGING_FILE = "DATA_511/completed_packaging.json"
BATCH_SIZE = 10 


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_message(message, level="info"):
    if level == "error":
        logging.error(message)
    else:
        logging.info(message)
    print(message)

def load_input_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log_message(f"Error loading JSON file: {e}", "error")
        return []
    
def append_to_csv(results, filename=OUTPUT_CSV_FILE):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['packaging_name', 'domain']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for row in results:
            writer.writerow(row)
    log_message(f"Appended {len(results)} entries to CSV file.")

def append_to_json(results, filename=OUTPUT_JSON_FILE):
    if os.path.exists(filename):
        with open(filename, 'r', encoding="utf-8") as jsonfile:
            try:
                existing_data = json.load(jsonfile)
            except json.JSONDecodeError:
                existing_data = {}
    else:
        existing_data = {}

    for row in results:
        name = row['packaging_name']
        domain = row['domain']
        if name not in existing_data:
            existing_data[name] = []
        existing_data[name].append(domain)

    with open(filename, 'w', encoding="utf-8") as jsonfile:
        json.dump(existing_data, jsonfile, indent=4)
    log_message(f"Appended {len(results)} entries to JSON file.")

def load_completed_packaging():
    if os.path.exists(COMPLETED_PACKAGING_FILE):
        with open(COMPLETED_PACKAGING_FILE, "r", encoding="utf-8") as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

def save_completed_packaging(completed):
    with open(COMPLETED_PACKAGING_FILE, "w", encoding="utf-8") as f:
        json.dump(list(completed), f, indent=4)

def get_domain_from_url(url):
    try:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        common_subdomains = ["www.", "ww.", "wwww.", "m.", "web."]
        for subdomain in common_subdomains:
            if domain.startswith(subdomain):
                domain = domain[len(subdomain):]
                break
        return domain
    except Exception as e:
        log_message(f"Error extracting domain from URL {url}: {e}", "error")
        return None

def restricted_domain(domain: str) -> bool:
    restricted_words = [
        "news", ".org", ".edu", ".gov", "tribune", "report"
    ]
    restricted_domains = [
        "dnb.com", "linkedin.com", "facebook.com", "bloomberg.com", "keychain.com",
        "safer.fmcsa.dot.gov", "fda.gov", "thomasnet.com", "opencorporates.com",
        "en.wikipedia.org", "wikipedia.org", "wikipedia.com", "manta.com",
        "fsis.usda.gov", "usda.gov", "yelp.com", "panjiva.com", "va.gov", "emis.com",
        "zoominfo.com", "facebook.com", "producemarketguide.com", "crunchbase.com",
        "pitchbook.com", "health.usnews.com", "usnews.com", "buzzfile.com",
        "6sense.com", "researchgate.net", "download.skype.com", "skype.com", "bbb.org",
        "volza.com", "healthgrades.com", "interfishmarket.com", "taiwantrade.com",
        "fisheries.msc.org", "asc-aqua.org", "sec.gov", "bbs.fobshanghai.com",
        "yellowpages.com", "instagram.com", "indiamart.com", "fda.report",
        "importgenius.com", "dairyfoods.com", "tripadvisor.com", "discovery-patsnap-com.libproxy.mit.edu",
        "ccof.org", "bakingbusiness.com", "justice.gov", "specialtyfood.com",
        "us.asc-aqua.org", "accessdata.fda.gov", "doctor.webmd.com", "en.52wmb.com",
        "52wmb.com", "in.linkedin.com", "seafood.media", "ncbi.nlm.nih.gov",
        "seafoodsource.com", "cphi-online.com", "europages.co.uk", "landmatrix.org",
        "dandb.com", "web.tcfa.org", "business.abidjan.net", "youtube.com",
        "uk.linkedin.com", "reddit.com", "ca.linkedin.com", "visualvisitor.com",
        "ci.linkedin.com", "il.linkedin.com", "au.linkedin.com", "be.linkedin.com",
        "br.linkedin.com", "pk.linkedin.com", "za.linkedin.com", "bg.linkedin.com",
        "nl.linkedin.com", "gr.linkedin.com", "sg.linkedin.com", "ie.linkedin.com",
        "ar.linkedin.com", "vn.linkedin.com", "id.linkedin.com", "hk.linkedin.com",
        "fr.linkedin.com", "mg.linkedin.com", "tiktok.com", "mx.linkedin.com",
        "it.linkedin.com", "gh.linkedin.com", "is.linkedin.com", "ng.linkedin.com",
        "es.linkedin.com", "co.linkedin.com", "ge.linkedin.com", "lk.linkedin.com",
        "pe.linkedin.com", "cl.linkedin.com", "pr.linkedin.com", "cn.linkedin.com",
        "instagram.com", "ch.linkedin.com", "hu.linkedin.com", "tr.linkedin.com",
        "hr.linkedin.com", "sk.linkedin.com", "fi.linkedin.com", "ir.linkedin.com",
        "gt.linkedin.com", "de.linkedin.com", "rs.linkedin.com", "nl-nl.facebook.com",
        "uz.linkedin.com", "pt.linkedin.com", "ec.linkedin.com", "se.linkedin.com",
        "mm.linkedin.com", "am.linkedin.com", "ba.linkedin.com", "x.facebook.com",
        "by.linkedin.com", "ae.linkedin.com", "ru.linkedin.com", "cz.linkedin.com",
        "im.linkedin.com", "pf.linkedin.com", "kr.linkedin.com", "ke.linkedin.com",
        "pl.linkedin.com", "sn.linkedin.com", "tz.linkedin.com", "lt.linkedin.com",
        "me.linkedin.com", "https://facebook.com/Blinzi-298817753975935",
        "lu.linkedin.com", "et.linkedin.com", "tj.linkedin.com", "bj.linkedin.com",
        "ht.linkedin.com", "facebook.com/camposdeolmue", "ug.linkedin.com",
        "lv.linkedin.com", "facebook.com/katkokoru", "mn.linkedin.com",
        "facebook.com/Sunrise-Farms-LLC", "bd.linkedin.com", "tt.linkedin.com",
        "bt.linkedin.com", "ph.linkedin.com", "kz.linkedin.com",
        "https://facebook.com/pages/Rainbow-Farms-Egg-Sales", "sz.linkedin.com",
        "facebook.com/SoliteVietnam", "mv.linkedin.com", "vc.linkedin.com",
        "l.facebook.com", "es-la.facebook.com", "kh.linkedin.com", "at.linkedin.com",
        "ms-my.facebook.com", "ee.linkedin.com", "sl.linkedin.com", "fo.linkedin.com",
        "hn.linkedin.com", "do.linkedin.com", "mt.linkedin.com", "he-il.facebook.com",
        "facebook.com/TOPEGGS", "dj.linkedin.com", "bi.linkedin.com", "tm.linkedin.com",
        "nz.linkedin.com", "cy.linkedin.com", "zm.linkedin.com", "ro.linkedin.com",
        "dk.linkedin.com", "nc.linkedin.com", "si.linkedin.com", "yahoo.com",
        "yahoo.co.jp", "yahoo.co.uk", "yahoo.co.in", "yahoo.com.br", "yahoo.com.mx",
        "yahoo.com.ar", "mordorintelligence.com", "market.us", "amazon.com",
        "reddit.com", "linkedin.com", "quora.com", "nih.gov", "youtube.com",
        "kroger.com", "walmart.com", "target.com", "fda.gov", "smithsfoodanddrug.com"
    ]
    if any(rd in domain for rd in restricted_domains):
        return True
    if any(rw in domain for rw in restricted_words):
        return True
    return False

def get_top_manufacturers_for_packaging(packaging_name):
    headers = {'Content-Type': 'application/json', 'X-API-Key': SERPER_API_KEY}
    all_manufacturers = []
    page = 1

    log_message(f"Fetching results for: {packaging_name}")

    while len(all_manufacturers) < 200:
        payload = {
            'q': f"Top {packaging_name} Suppliers in the United States",
            'gl': 'us',
            'num': 10,
            'page': page  
        }
        response = requests.post(SERPER_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            if 'organic' in response_data:
                for organic_result in response_data['organic']:
                    domain = get_domain_from_url(organic_result.get('link', ''))
                    if domain and not restricted_domain(domain):
                        all_manufacturers.append(domain)
            elif 'knowledge_graph' in response_data:
                domain = get_domain_from_url(response_data['knowledge_graph'].get('website', ''))
                if domain and not restricted_domain(domain):
                    all_manufacturers.append(domain)
        else:
            log_message(f"Error: Failed to fetch results for '{packaging_name}'. Status code: {response.status_code}", "error")
            print(response.text)
            break  

        page += 1  

    log_message(f"Found {len(all_manufacturers)} manufacturers for: {packaging_name}")
    return packaging_name, all_manufacturers[:200]

def get_top_manufacturers(input_data, max_threads=5):
    completed_packaging = load_completed_packaging()
    results = []
    batch_results = []

    with ThreadPoolExecutor(max_threads) as executor:
        futures = {
            executor.submit(get_top_manufacturers_for_packaging, row['name']): row['name']
            for row in input_data if row['name'] not in completed_packaging
        }
        for future in tqdm(as_completed(futures), total=len(futures), desc="Fetching Websites"):
            try:
                packaging_name, top_manufacturers = future.result()
                for manufacturer in top_manufacturers:
                    batch_results.append({
                        "packaging_name": packaging_name,
                        "domain": manufacturer
                    })
                completed_packaging.add(packaging_name)
                save_completed_packaging(completed_packaging)

                if len(batch_results) >= BATCH_SIZE:
                    append_to_csv(batch_results)
                    append_to_json(batch_results)
                    results.extend(batch_results)
                    batch_results = []

                    log_message(f"Saved a batch of {BATCH_SIZE} results to files.")

            except Exception as e:
                packaging_name = futures[future]
                log_message(f"Error processing '{packaging_name}': {e}", "error")

    if batch_results:
        append_to_csv(batch_results)
        append_to_json(batch_results)
        results.extend(batch_results)
        log_message("Final batch saved.")

    return results

if __name__ == "__main__":
    log_message("Starting script execution.")
    input_data = load_input_data(INPUT_JSON_FILE)
    
    if not input_data:
        log_message("No input data found. Exiting.", "error")
        exit()

    top_manufacturers = get_top_manufacturers(input_data)

    log_message(f"Top 200 websites per name saved to {OUTPUT_JSON_FILE} and {OUTPUT_CSV_FILE}")
    log_message("Script execution completed.")
