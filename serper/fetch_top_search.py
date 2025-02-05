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

output_file = 'serper/DATA_332/120_/serper_final.json'


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
    "index": 121,
    "packaging_name": "Pan",
    "material_name": "Misc Material",
    "products_tagged": 23
  },
  {
    "index": 122,
    "packaging_name": "Brick",
    "material_name": "Plastic",
    "products_tagged": 22
  },
  {
    "index": 123,
    "packaging_name": "Longneck Bottle",
    "material_name": "Aluminum",
    "products_tagged": 20
  },
  {
    "index": 124,
    "packaging_name": "Box",
    "material_name": "Wood",
    "products_tagged": 20
  },
  {
    "index": 125,
    "packaging_name": "Tube",
    "material_name": "Cardboard",
    "products_tagged": 19
  },
  {
    "index": 126,
    "packaging_name": "Bottle In Box",
    "material_name": "Misc Material",
    "products_tagged": 18
  },
  {
    "index": 127,
    "packaging_name": "Box",
    "material_name": "Metal",
    "products_tagged": 18
  },
  {
    "index": 128,
    "packaging_name": "Wrap In Box",
    "material_name": "Cardboard",
    "products_tagged": 16
  },
  {
    "index": 129,
    "packaging_name": "Bowl",
    "material_name": "Coated Cardboard",
    "products_tagged": 15
  },
  {
    "index": 130,
    "packaging_name": "Envelope In Box",
    "material_name": "Plastic",
    "products_tagged": 15
  },
  {
    "index": 131,
    "packaging_name": "Bag",
    "material_name": "Coated Cardboard",
    "products_tagged": 15
  },
  {
    "index": 132,
    "packaging_name": "Box",
    "material_name": "Paper",
    "products_tagged": 15
  },
  {
    "index": 133,
    "packaging_name": "Cask In Box",
    "material_name": "Cardboard",
    "products_tagged": 14
  },
  {
    "index": 134,
    "packaging_name": "Bottle",
    "material_name": "Ceramic",
    "products_tagged": 14
  },
  {
    "index": 135,
    "packaging_name": "Platter",
    "material_name": "Plastic",
    "products_tagged": 14
  },
  {
    "index": 136,
    "packaging_name": "Tube In Box",
    "material_name": "Cardboard",
    "products_tagged": 13
  },
  {
    "index": 137,
    "packaging_name": "Molded Tray",
    "material_name": "Misc Material",
    "products_tagged": 12
  },
  {
    "index": 138,
    "packaging_name": "Tray",
    "material_name": "Metal",
    "products_tagged": 12
  },
  {
    "index": 139,
    "packaging_name": "Carton",
    "material_name": "Misc Material",
    "products_tagged": 12
  },
  {
    "index": 140,
    "packaging_name": "Box",
    "material_name": "Coated Paper",
    "products_tagged": 11
  },
  {
    "index": 141,
    "packaging_name": "Case",
    "material_name": "Plastic",
    "products_tagged": 11
  },
  {
    "index": 142,
    "packaging_name": "Can",
    "material_name": "Glass",
    "products_tagged": 11
  },
  {
    "index": 143,
    "packaging_name": "Tray In Sleeve",
    "material_name": "Misc Material",
    "products_tagged": 11
  },
  {
    "index": 144,
    "packaging_name": "Canister",
    "material_name": "Coated Cardboard",
    "products_tagged": 10
  },
  {
    "index": 145,
    "packaging_name": "Keg",
    "material_name": "Metal",
    "products_tagged": 10
  },
  {
    "index": 146,
    "packaging_name": "Microwaveable",
    "material_name": "Coated Cardboard",
    "products_tagged": 10
  },
  {
    "index": 147,
    "packaging_name": "Wrap",
    "material_name": "Wax",
    "products_tagged": 10
  },
  {
    "index": 148,
    "packaging_name": "Bottle",
    "material_name": "Coated Cardboard",
    "products_tagged": 9
  },
  {
    "index": 149,
    "packaging_name": "Bag",
    "material_name": "Cloth",
    "products_tagged": 9
  },
  {
    "index": 150,
    "packaging_name": "Pouch",
    "material_name": "Bpa Free Plastic",
    "products_tagged": 9
  },
  {
    "index": 151,
    "packaging_name": "Misc Packaging Format",
    "material_name": "Cellophane",
    "products_tagged": 9
  },
  {
    "index": 152,
    "packaging_name": "Jar",
    "material_name": "Cardboard",
    "products_tagged": 9
  },
  {
    "index": 153,
    "packaging_name": "Bowl In Sleeve",
    "material_name": "Plastic",
    "products_tagged": 9
  },
  {
    "index": 154,
    "packaging_name": "Box",
    "material_name": "Tin",
    "products_tagged": 7
  },
  {
    "index": 155,
    "packaging_name": "Tub In Sleeve",
    "material_name": "Plastic",
    "products_tagged": 7
  },
  {
    "index": 156,
    "packaging_name": "Keg",
    "material_name": "Aluminum",
    "products_tagged": 7
  },
  {
    "index": 157,
    "packaging_name": "Longneck Bottle In Box",
    "material_name": "Glass",
    "products_tagged": 6
  },
  {
    "index": 158,
    "packaging_name": "Bottle In Canister",
    "material_name": "Metal",
    "products_tagged": 6
  },
  {
    "index": 159,
    "packaging_name": "Sleeve",
    "material_name": "Misc Material",
    "products_tagged": 6
  },
  {
    "index": 160,
    "packaging_name": "Molded Tray",
    "material_name": "Plastic",
    "products_tagged": 6
  },
  {
    "index": 161,
    "packaging_name": "Tube",
    "material_name": "Foil",
    "products_tagged": 6
  },
  {
    "index": 162,
    "packaging_name": "Canister",
    "material_name": "Glass",
    "products_tagged": 6
  },
  {
    "index": 163,
    "packaging_name": "Bottle In Box",
    "material_name": "Ceramic",
    "products_tagged": 6
  },
  {
    "index": 164,
    "packaging_name": "Tray",
    "material_name": "Aluminum",
    "products_tagged": 6
  },
  {
    "index": 165,
    "packaging_name": "Canister",
    "material_name": "Coated Paper",
    "products_tagged": 6
  },
  {
    "index": 166,
    "packaging_name": "Pod",
    "material_name": "Plastic",
    "products_tagged": 6
  },
  {
    "index": 167,
    "packaging_name": "Microwaveable",
    "material_name": "Misc Material",
    "products_tagged": 6
  },
  {
    "index": 168,
    "packaging_name": "Bottle In Canister",
    "material_name": "Cardboard",
    "products_tagged": 6
  },
  {
    "index": 169,
    "packaging_name": "Bottle In Bag",
    "material_name": "Glass",
    "products_tagged": 6
  },
  {
    "index": 170,
    "packaging_name": "Canister In Wrap",
    "material_name": "Plastic",
    "products_tagged": 5
  },
  {
    "index": 171,
    "packaging_name": "Misc Packaging Format",
    "material_name": "Rubber",
    "products_tagged": 5
  },
  {
    "index": 172,
    "packaging_name": "Box In Wrap",
    "material_name": "Misc Material",
    "products_tagged": 5
  },
  {
    "index": 173,
    "packaging_name": "Stick In Box",
    "material_name": "Cardboard",
    "products_tagged": 5
  },
  {
    "index": 174,
    "packaging_name": "Bowl In Sleeve",
    "material_name": "Misc Material",
    "products_tagged": 5
  },
  {
    "index": 175,
    "packaging_name": "Brick",
    "material_name": "Coated Paper",
    "products_tagged": 5
  },
  {
    "index": 176,
    "packaging_name": "Carton",
    "material_name": "Coated Paper",
    "products_tagged": 5
  },
  {
    "index": 177,
    "packaging_name": "Cup",
    "material_name": "Cardboard",
    "products_tagged": 5
  },
  {
    "index": 178,
    "packaging_name": "Brick",
    "material_name": "Misc Material",
    "products_tagged": 5
  },
  {
    "index": 179,
    "packaging_name": "Wrap In Bag",
    "material_name": "Misc Material",
    "products_tagged": 4
  },
  {
    "index": 180,
    "packaging_name": "Cup",
    "material_name": "Paper",
    "products_tagged": 4
  },
  {
    "index": 181,
    "packaging_name": "Tub",
    "material_name": "Cellophane",
    "products_tagged": 4
  },
  {
    "index": 182,
    "packaging_name": "Bottle In Box",
    "material_name": "Plastic",
    "products_tagged": 4
  },
  {
    "index": 183,
    "packaging_name": "Short Neck Bottle",
    "material_name": "Plastic",
    "products_tagged": 4
  },
  {
    "index": 184,
    "packaging_name": "Tub",
    "material_name": "Styrofoam",
    "products_tagged": 4
  },
  {
    "index": 185,
    "packaging_name": "Envelope",
    "material_name": "Coated Cardboard",
    "products_tagged": 4
  },
  {
    "index": 186,
    "packaging_name": "Canister",
    "material_name": "Foil",
    "products_tagged": 4
  },
  {
    "index": 187,
    "packaging_name": "Envelope",
    "material_name": "Cellophane",
    "products_tagged": 4
  },
  {
    "index": 188,
    "packaging_name": "Pouch Bag",
    "material_name": "Plastic",
    "products_tagged": 3
  },
  {
    "index": 189,
    "packaging_name": "Carton",
    "material_name": "Glass",
    "products_tagged": 3
  },
  {
    "index": 190,
    "packaging_name": "Short Neck Bottle",
    "material_name": "Misc Material",
    "products_tagged": 3
  },
  {
    "index": 191,
    "packaging_name": "Jug",
    "material_name": "Cardboard",
    "products_tagged": 3
  },
  {
    "index": 192,
    "packaging_name": "Tray In Box",
    "material_name": "Plastic",
    "products_tagged": 3
  },
  {
    "index": 193,
    "packaging_name": "Wrap In Box",
    "material_name": "Plastic",
    "products_tagged": 3
  },
  {
    "index": 194,
    "packaging_name": "Tub",
    "material_name": "Wood",
    "products_tagged": 3
  },
  {
    "index": 195,
    "packaging_name": "Canister",
    "material_name": "Paper",
    "products_tagged": 3
  },
  {
    "index": 196,
    "packaging_name": "Tray In Sleeve",
    "material_name": "Cardboard",
    "products_tagged": 3
  },
  {
    "index": 197,
    "packaging_name": "Box",
    "material_name": "Waxed Cardboard",
    "products_tagged": 3
  },
  {
    "index": 198,
    "packaging_name": "Tray",
    "material_name": "Paper",
    "products_tagged": 3
  },
  {
    "index": 199,
    "packaging_name": "Bowl",
    "material_name": "Glass",
    "products_tagged": 3
  },
  {
    "index": 200,
    "packaging_name": "Bag In Box",
    "material_name": "Plastic",
    "products_tagged": 3
  },
  {
    "index": 201,
    "packaging_name": "Wide Mouth Can",
    "material_name": "Aluminum",
    "products_tagged": 3
  },
  {
    "index": 202,
    "packaging_name": "Tub",
    "material_name": "Coated Paper",
    "products_tagged": 3
  },
  {
    "index": 203,
    "packaging_name": "Ring",
    "material_name": "Plastic",
    "products_tagged": 3
  },
  {
    "index": 204,
    "packaging_name": "Wrap In Tray",
    "material_name": "Misc Material",
    "products_tagged": 3
  },
  {
    "index": 205,
    "packaging_name": "Misc Packaging Format",
    "material_name": "Mesh",
    "products_tagged": 3
  },
  {
    "index": 206,
    "packaging_name": "Tub",
    "material_name": "Metal",
    "products_tagged": 3
  },
  {
    "index": 207,
    "packaging_name": "Bottle In Box",
    "material_name": "Metal",
    "products_tagged": 2
  },
  {
    "index": 208,
    "packaging_name": "Bowl",
    "material_name": "Styrofoam",
    "products_tagged": 2
  },
  {
    "index": 209,
    "packaging_name": "Vented Wide Mouth Can",
    "material_name": "Aluminum",
    "products_tagged": 2
  },
  {
    "index": 210,
    "packaging_name": "Cup",
    "material_name": "Coated Paper",
    "products_tagged": 2
  },
  {
    "index": 211,
    "packaging_name": "Basket",
    "material_name": "Wicker",
    "products_tagged": 2
  },
  {
    "index": 212,
    "packaging_name": "Longneck Bottle",
    "material_name": "Plastic",
    "products_tagged": 2
  },
  {
    "index": 213,
    "packaging_name": "Bottle In Sleeve",
    "material_name": "Glass",
    "products_tagged": 2
  },
  {
    "index": 214,
    "packaging_name": "Box In Wrap",
    "material_name": "Plastic",
    "products_tagged": 2
  },
  {
    "index": 215,
    "packaging_name": "Tray",
    "material_name": "Coated Paper",
    "products_tagged": 2
  },
  {
    "index": 216,
    "packaging_name": "Envelope In Bag",
    "material_name": "Plastic",
    "products_tagged": 2
  },
  {
    "index": 217,
    "packaging_name": "Well",
    "material_name": "Plastic",
    "products_tagged": 2
  },
  {
    "index": 218,
    "packaging_name": "Pouch",
    "material_name": "Cardboard",
    "products_tagged": 2
  },
  {
    "index": 219,
    "packaging_name": "Bowl In Box",
    "material_name": "Plastic",
    "products_tagged": 2
  },
  {
    "index": 220,
    "packaging_name": "Pan",
    "material_name": "Metal",
    "products_tagged": 2
  },
  {
    "index": 221,
    "packaging_name": "Bowl",
    "material_name": "Paper",
    "products_tagged": 2
  },
  {
    "index": 222,
    "packaging_name": "Grinder",
    "material_name": "Misc Material",
    "products_tagged": 2
  },
  {
    "index": 223,
    "packaging_name": "Carton",
    "material_name": "Plastic",
    "products_tagged": 2
  },
  {
    "index": 224,
    "packaging_name": "Basket",
    "material_name": "Plastic",
    "products_tagged": 2
  },
  {
    "index": 225,
    "packaging_name": "Wrap",
    "material_name": "Poly",
    "products_tagged": 2
  },
  {
    "index": 226,
    "packaging_name": "Bottle",
    "material_name": "Bpa Free Plastic",
    "products_tagged": 2
  },
  {
    "index": 227,
    "packaging_name": "Wrap",
    "material_name": "Mesh",
    "products_tagged": 2
  },
  {
    "index": 228,
    "packaging_name": "Carded",
    "material_name": "Coated Cardboard",
    "products_tagged": 2
  },
  {
    "index": 229,
    "packaging_name": "Microwaveable",
    "material_name": "Aluminum",
    "products_tagged": 1
  },
  {
    "index": 230,
    "packaging_name": "Tube In Box",
    "material_name": "Misc Material",
    "products_tagged": 1
  },
  {
    "index": 231,
    "packaging_name": "Tin",
    "material_name": "Plastic",
    "products_tagged": 1
  },
  {
    "index": 232,
    "packaging_name": "Wrap In Tray",
    "material_name": "Plastic",
    "products_tagged": 1
  },
  {
    "index": 233,
    "packaging_name": "Wide Mouth Short Neck Bottle",
    "material_name": "Aluminum",
    "products_tagged": 1
  },
  {
    "index": 234,
    "packaging_name": "Carded",
    "material_name": "Cellophane",
    "products_tagged": 1
  },
  {
    "index": 235,
    "packaging_name": "Misc Packaging Format",
    "material_name": "Fabric",
    "products_tagged": 1
  },
  {
    "index": 236,
    "packaging_name": "Stick Pack",
    "material_name": "Cardboard",
    "products_tagged": 1
  },
  {
    "index": 237,
    "packaging_name": "Misc Packaging Format",
    "material_name": "Brown Coated Paper",
    "products_tagged": 1
  },
  {
    "index": 238,
    "packaging_name": "Misc Packaging Format",
    "material_name": "Steel",
    "products_tagged": 1
  },
  {
    "index": 239,
    "packaging_name": "Stick In Canister",
    "material_name": "Metal",
    "products_tagged": 1
  },
  {
    "index": 240,
    "packaging_name": "Tray",
    "material_name": "Wood",
    "products_tagged": 1
  },
  {
    "index": 241,
    "packaging_name": "Keg",
    "material_name": "Steel",
    "products_tagged": 1
  },
  {
    "index": 242,
    "packaging_name": "Bottle In Basket",
    "material_name": "Glass",
    "products_tagged": 1
  },
  {
    "index": 243,
    "packaging_name": "Misc Packaging Format",
    "material_name": "Styrofoam",
    "products_tagged": 1
  },
  {
    "index": 244,
    "packaging_name": "Wrap In Sleeve",
    "material_name": "Misc Material",
    "products_tagged": 1
  },
  {
    "index": 245,
    "packaging_name": "Box In Wrap",
    "material_name": "Coated Cardboard",
    "products_tagged": 1
  },
  {
    "index": 246,
    "packaging_name": "Basket",
    "material_name": "Cardboard",
    "products_tagged": 1
  },
  {
    "index": 247,
    "packaging_name": "Envelope In Tray",
    "material_name": "Plastic",
    "products_tagged": 1
  },
  {
    "index": 248,
    "packaging_name": "Tray In Box",
    "material_name": "Cardboard",
    "products_tagged": 1
  },
  {
    "index": 249,
    "packaging_name": "Box",
    "material_name": "Aluminum",
    "products_tagged": 1
  },
  {
    "index": 250,
    "packaging_name": "Bag In Box",
    "material_name": "Misc Material",
    "products_tagged": 1
  },
  {
    "index": 251,
    "packaging_name": "Bottle In Bag",
    "material_name": "Plastic",
    "products_tagged": 1
  },
  {
    "index": 252,
    "packaging_name": "Baby Bottle",
    "material_name": "Misc Material",
    "products_tagged": 1
  },
  {
    "index": 253,
    "packaging_name": "Packet",
    "material_name": "Paper",
    "products_tagged": 1
  },
  {
    "index": 254,
    "packaging_name": "Pouch",
    "material_name": "Coated Paper",
    "products_tagged": 1
  },
  {
    "index": 255,
    "packaging_name": "Pod",
    "material_name": "Coated Cardboard",
    "products_tagged": 1
  },
  {
    "index": 256,
    "packaging_name": "Flask",
    "material_name": "Metal",
    "products_tagged": 1
  },
  {
    "index": 257,
    "packaging_name": "Basket",
    "material_name": "Wood",
    "products_tagged": 1
  },
  {
    "index": 258,
    "packaging_name": "Tube Envelope In Box",
    "material_name": "Plastic",
    "products_tagged": 1
  },
  {
    "index": 259,
    "packaging_name": "Envelope In Box",
    "material_name": "Coated Paper",
    "products_tagged": 1
  },
  {
    "index": 260,
    "packaging_name": "Sleeve",
    "material_name": "Coated Paper",
    "products_tagged": 1
  },
  {
    "index": 261,
    "packaging_name": "Pegged",
    "material_name": "Plastic",
    "products_tagged": 1
  },
  {
    "index": 262,
    "packaging_name": "Tube In Box",
    "material_name": "Glass",
    "products_tagged": 1
  },
  {
    "index": 263,
    "packaging_name": "Sachet In Box",
    "material_name": "Cardboard",
    "products_tagged": 1
  },
  {
    "index": 264,
    "packaging_name": "Tray In Wrap",
    "material_name": "Misc Material",
    "products_tagged": 1
  },
  {
    "index": 265,
    "packaging_name": "Tray",
    "material_name": "Waxed Cardboard",
    "products_tagged": 1
  },
  {
    "index": 266,
    "packaging_name": "Box In Sleeve",
    "material_name": "Misc Material",
    "products_tagged": 1
  },
  {
    "index": 267,
    "packaging_name": "Bottle",
    "material_name": "Paper",
    "products_tagged": 1
  },
  {
    "index": 268,
    "packaging_name": "Bag In Box",
    "material_name": "Paper",
    "products_tagged": 1
  },
  {
    "index": 269,
    "packaging_name": "Vial",
    "material_name": "Plastic",
    "products_tagged": 1
  },
  {
    "index": 270,
    "packaging_name": "Tube Envelope In Box",
    "material_name": "Cardboard",
    "products_tagged": 1
  },
  {
    "index": 271,
    "packaging_name": "Basket",
    "material_name": "Bamboo",
    "products_tagged": 1
  },
  {
    "index": 272,
    "packaging_name": "Tube Envelope",
    "material_name": "Plastic",
    "products_tagged": 1
  },
  {
    "index": 273,
    "packaging_name": "Big Mouth Short Neck Bottle",
    "material_name": "Glass",
    "products_tagged": 1
  },
  {
    "index": 274,
    "packaging_name": "Tray In Wrap",
    "material_name": "Cardboard",
    "products_tagged": 1
  },
  {
    "index": 275,
    "packaging_name": "Bottle In Bag",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 276,
    "packaging_name": "Basket",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 277,
    "packaging_name": "Sachet In Box",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 278,
    "packaging_name": "Tote",
    "material_name": "Poly",
    "products_tagged": 0
  },
  {
    "index": 279,
    "packaging_name": "Carton",
    "material_name": "Elopak",
    "products_tagged": 0
  },
  {
    "index": 280,
    "packaging_name": "Wide Mouth Can",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 281,
    "packaging_name": "Jar In Wrap",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 282,
    "packaging_name": "Dropper Bottle",
    "material_name": "Aluminum",
    "products_tagged": 0
  },
  {
    "index": 283,
    "packaging_name": "Tray In Box",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 284,
    "packaging_name": "Dropper Bottle",
    "material_name": "Plastic",
    "products_tagged": 0
  },
  {
    "index": 285,
    "packaging_name": "Stick In Canister",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 286,
    "packaging_name": "Pod",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 287,
    "packaging_name": "Tin",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 288,
    "packaging_name": "Bottle In Sleeve",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 289,
    "packaging_name": "Tub In Sleeve",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 290,
    "packaging_name": "Bottle In Wrap",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 291,
    "packaging_name": "Envelope In Tray",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 292,
    "packaging_name": "Dropper Bottle",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 293,
    "packaging_name": "Tube Envelope",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 294,
    "packaging_name": "Carton",
    "material_name": "SIG Combibloc",
    "products_tagged": 0
  },
  {
    "index": 295,
    "packaging_name": "Bowl In Box",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 296,
    "packaging_name": "Packet",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 297,
    "packaging_name": "Bag",
    "material_name": "Multi-wall paper",
    "products_tagged": 0
  },
  {
    "index": 298,
    "packaging_name": "Tube Envelope In Box",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 299,
    "packaging_name": "Stick Pack",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 300,
    "packaging_name": "Recart Carton",
    "material_name": "TetraPak",
    "products_tagged": 0
  },
  {
    "index": 301,
    "packaging_name": "Pouch Bag",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 302,
    "packaging_name": "Jug",
    "material_name": "HDPE",
    "products_tagged": 0
  },
  {
    "index": 303,
    "packaging_name": "Vial",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 304,
    "packaging_name": "Keg",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 305,
    "packaging_name": "Bottle In Basket",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 306,
    "packaging_name": "Jug",
    "material_name": "PET",
    "products_tagged": 0
  },
  {
    "index": 307,
    "packaging_name": "Envelope In Bag",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 308,
    "packaging_name": "Case",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 309,
    "packaging_name": "Bottle In Canister",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 310,
    "packaging_name": "Longneck Bottle In Box",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 311,
    "packaging_name": "Wide Mouth Short Neck Bottle",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 312,
    "packaging_name": "Dropper Bottle",
    "material_name": "Glass",
    "products_tagged": 0
  },
  {
    "index": 313,
    "packaging_name": "Big Mouth Short Neck Bottle",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 314,
    "packaging_name": "Flask",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 315,
    "packaging_name": "Can",
    "material_name": "Nitro",
    "products_tagged": 0
  },
  {
    "index": 316,
    "packaging_name": "Canister In Wrap",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 317,
    "packaging_name": "Cask In Box",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 318,
    "packaging_name": "Vented Wide Mouth Can",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 319,
    "packaging_name": "Theater Box",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 320,
    "packaging_name": "Stick In Box",
    "material_name": "Misc Material",
    "products_tagged": 0
  },
  {
    "index": 321,
    "packaging_name": "Bottle",
    "material_name": "PET",
    "products_tagged": 0
  }
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
