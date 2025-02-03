import requests
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

output_file = 'serper/DATA_332/41_80/serper_41_80.json'


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


input_data = [
   {
    "index": 41,
    "packaging_name": "Wrap",
    "material_name": "Cardboard",
    "products_tagged": 695
  },
  {
    "index": 42,
    "packaging_name": "Envelope",
    "material_name": "Plastic",
    "products_tagged": 665
  },
  {
    "index": 43,
    "packaging_name": "Pegged",
    "material_name": "Misc Material",
    "products_tagged": 616
  },
  {
    "index": 44,
    "packaging_name": "Box",
    "material_name": "Coated Cardboard",
    "products_tagged": 615
  },
  {
    "index": 45,
    "packaging_name": "Envelope",
    "material_name": "Misc Material",
    "products_tagged": 604
  },
  {
    "index": 46,
    "packaging_name": "Carton",
    "material_name": "Coated Cardboard",
    "products_tagged": 536
  },
  {
    "index": 47,
    "packaging_name": "Bag",
    "material_name": "Cellophane",
    "products_tagged": 522
  },
  {
    "index": 48,
    "packaging_name": "Canister",
    "material_name": "Cardboard",
    "products_tagged": 428
  },
  {
    "index": 49,
    "packaging_name": "Envelope",
    "material_name": "Foil",
    "products_tagged": 412
  },
  {
    "index": 50,
    "packaging_name": "Wrap",
    "material_name": "Paper",
    "products_tagged": 405
  },
  {
    "index": 51,
    "packaging_name": "Can",
    "material_name": "Steel",
    "products_tagged": 395
  },
  {
    "index": 52,
    "packaging_name": "Tube",
    "material_name": "Plastic",
    "products_tagged": 385
  },
  {
    "index": 53,
    "packaging_name": "Cup",
    "material_name": "Plastic",
    "products_tagged": 355
  },
  {
    "index": 54,
    "packaging_name": "Microwaveable",
    "material_name": "Plastic",
    "products_tagged": 255
  },
  {
    "index": 55,
    "packaging_name": "Misc Packaging Format",
    "material_name": "Metal",
    "products_tagged": 250
  },
  {
    "index": 56,
    "packaging_name": "Bottle In Box",
    "material_name": "Glass",
    "products_tagged": 242
  },
  {
    "index": 57,
    "packaging_name": "Tray",
    "material_name": "Styrofoam",
    "products_tagged": 234
  },
  {
    "index": 58,
    "packaging_name": "Jug",
    "material_name": "Misc Material",
    "products_tagged": 234
  },
  {
    "index": 59,
    "packaging_name": "Tray",
    "material_name": "Cardboard",
    "products_tagged": 232
  },
  {
    "index": 60,
    "packaging_name": "Jug",
    "material_name": "Plastic",
    "products_tagged": 224
  },
  {
    "index": 61,
    "packaging_name": "Short Neck Bottle",
    "material_name": "Glass",
    "products_tagged": 222
  },
  {
    "index": 62,
    "packaging_name": "Can",
    "material_name": "Cardboard",
    "products_tagged": 220
  },
  {
    "index": 63,
    "packaging_name": "Bag In Box",
    "material_name": "Cardboard",
    "products_tagged": 207
  },
  {
    "index": 64,
    "packaging_name": "Theater Box",
    "material_name": "Cardboard",
    "products_tagged": 198
  },
  {
    "index": 65,
    "packaging_name": "Bottle",
    "material_name": "Cardboard",
    "products_tagged": 175
  },
  {
    "index": 66,
    "packaging_name": "Misc Packaging Format",
    "material_name": "Misc Material",
    "products_tagged": 168
  },
  {
    "index": 67,
    "packaging_name": "Carded",
    "material_name": "Cardboard",
    "products_tagged": 156
  },
  {
    "index": 68,
    "packaging_name": "Can",
    "material_name": "Plastic",
    "products_tagged": 152
  },
  {
    "index": 69,
    "packaging_name": "Envelope In Box",
    "material_name": "Cardboard",
    "products_tagged": 143
  },
  {
    "index": 70,
    "packaging_name": "Envelope",
    "material_name": "Cardboard",
    "products_tagged": 141
  },
  {
    "index": 71,
    "packaging_name": "Bag",
    "material_name": "Brown Paper",
    "products_tagged": 131
  },
  {
    "index": 72,
    "packaging_name": "Pouch",
    "material_name": "Misc Material",
    "products_tagged": 130
  },
  {
    "index": 73,
    "packaging_name": "Bag",
    "material_name": "Poly",
    "products_tagged": 123
  },
  {
    "index": 74,
    "packaging_name": "Bottle In Wrap",
    "material_name": "Plastic",
    "products_tagged": 118
  },
  {
    "index": 75,
    "packaging_name": "Bowl",
    "material_name": "Plastic",
    "products_tagged": 106
  },
  {
    "index": 76,
    "packaging_name": "Envelope",
    "material_name": "Paper",
    "products_tagged": 106
  },
  {
    "index": 77,
    "packaging_name": "Grinder",
    "material_name": "Glass",
    "products_tagged": 97
  },
  {
    "index": 78,
    "packaging_name": "Tub",
    "material_name": "Cardboard",
    "products_tagged": 92
  },
  {
    "index": 79,
    "packaging_name": "Bottle",
    "material_name": "Aluminum",
    "products_tagged": 86
  },
  {
    "index": 80,
    "packaging_name": "Envelope",
    "material_name": "Coated Paper",
    "products_tagged": 81
  },
]

def get_top_manufacturers_for_packaging(packaging_name):
    headers = {'Content-Type': 'application/json', 'X-API-Key': SERPER_API_KEY}
    payload = {
        'q': f"Top {packaging_name} manufacturers in United States",
        'gl': 'us',
        'num': 200
    }
    response = requests.post(SERPER_API_URL, json=payload, headers=headers)
    top_manufacturers = []
    if response.status_code == 200:
        response_data = response.json()
        if 'organic' in response_data:
            for organic_result in response_data['organic']:
                domain = get_domain_from_url(organic_result.get('link', ''))
                if domain and not restricted_domain(domain):
                    top_manufacturers.append(domain)
        elif 'knowledge_graph' in response_data:
            domain = get_domain_from_url(response_data['knowledge_graph'].get('website', ''))
            if domain and not restricted_domain(domain):
                top_manufacturers.append(domain)
        else:
            print(f"Warning: Unexpected response structure for '{packaging_name}' in the USA.")
    else:
        print(f"Error: Failed to fetch results for '{packaging_name}' in the USA. Status code: {response.status_code}")
    return packaging_name, top_manufacturers

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
        print(f"Error extracting domain from URL {url}: {e}")
        return None

def save_to_csv(results, filename=output_file):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['packaging_name', 'domain']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

def save_to_json(results, filename=output_file):
    with open(filename, 'w') as jsonfile:
        json.dump(results, jsonfile)

def get_top_manufacturers(max_threads=10):
    results = []
    with ThreadPoolExecutor(max_threads) as executor:
        futures = {
            executor.submit(get_top_manufacturers_for_packaging, row['material_name'] + ' ' + row['packaging_name']): row['material_name'] + ' ' + row['packaging_name']
            for row in input_data
        }
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing Categories"):
            try:
                packaging_name, top_manufacturers = future.result()
                for manufacturer in top_manufacturers:
                    results.append({
                        "packaging_name": packaging_name,
                        "domain": manufacturer
                    })
            except Exception as e:
                packaging_name = futures[future]
                print(f"Error processing '{packaging_name}' in the USA: {e}")
    return results

if __name__ == "__main__":
    top_manufacturers = get_top_manufacturers()
    # save_to_csv(top_manufacturers)
    save_to_json(top_manufacturers)
