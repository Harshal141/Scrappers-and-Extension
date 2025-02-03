import csv
import json
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
load_dotenv()
MAX_WORKERS = 40
SERPER_API_URL = "https://google.serper.dev/search"
SERPER_API_KEY = os.getenv("SERPER_API_KEY_V2")
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

def get_domain_from_url(url):
    """
    Extract the domain from a URL.
    """
    try:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        # Remove common subdomains
        common_subdomains = ["www.", "ww.", "wwww.", "m.", "web."]
        for subdomain in common_subdomains:
            if domain.startswith(subdomain):
                domain = domain[len(subdomain):]
                break  # No need to check further once a match is found
        return domain
    except Exception as e:
        print(f"Error occurred while getting domain for URL {url}: {e}")
        return None
def search_company_domain_using_serper(company_name: str):
    headers = {"Content-Type": "application/json", "X-API-Key": SERPER_API_KEY}
    payload = {
        "q": f"{company_name} official site",
        "location": "Canada",
        "num": 10,
        "gl": "ca",
    }
    response = requests.post(SERPER_API_URL, json=payload, headers=headers)
    domain = ""
    if response.status_code == 200:
        response_data = response.json()
        url_index = 0
        while domain == "" and url_index < len(response_data["organic"]):
            if "organic" in response_data and response_data["organic"]:
                domain = get_domain_from_url(response_data["organic"][url_index]["link"])
                if restricted_domain(domain):
                    domain = ""
                url_index += 1
            else:
                print(
                    f"Warning: Unexpected response structure for company '{company_name}'."
                )
                break
    else:
        print(
            f"Error: Failed to fetch results for company '{company_name}'.Status code: {response.status_code}"
        )
    # print(company_name, domain, response_data["organic"][0]["link"])
    return domain

if __name__ == "__main__":
    with open("expowest/unique_data.json", "r") as file:
        data = json.load(file)

    names = [row["name"] for row in data]
    print(len(names))
    print(names[:10])
    # with open("scraping/scripts/output/sqf_canada_nov_2024.csv", "r") as file:
    #     names = [row[0] for row in csv.reader(file)]

    with open("expowest/serper_domains.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Facility Name", "Domain"])
        for name in names:
            domain = search_company_domain_using_serper(name)
            if not domain or domain == "":
                continue
            writer.writerow([name, domain])
            print(f"{name}: {domain}")