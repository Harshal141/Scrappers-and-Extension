from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from utility import cleanDomain

# List of URLs
urls = ['https://www.prosource.org/company/advanced-poly-packaging-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/amcor-flexibles-north-america?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/american-fuji-seal-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/anchor-packaging?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/aplix-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/aripack?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/cam-packaging-systems?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/candk-propack?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/celplast-metallized-products-limited?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/charter-next-generation?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/cheer-pack-north-america?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/clysar-llc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/colormasters-llc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/constantia-flexibles?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/duraco-specialty-materials?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/eagle-flexible-packaging?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/elplast-group?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/evergreen-resources?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/film-source-packaging?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/flex-films-usa-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/flexo-cristal-de-mexico?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/fres-co-system-usa-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/glenroy-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/hpm-global-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/idemitsu-unitech-co-ltd?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/iljin-gratec-usa-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/impak-corporation?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/knack-packaging?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/lasx?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/mondi?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/morris-packaging?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/multivac-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/pac-machinery?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/packaging-personified-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/parkside-flexibles-limited?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/paxxus?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/peel-plastics?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/pennpac?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/plastic-packaging-technologies-llc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/polyplex-usa-llc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/pregis-llc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/presto-products-company?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/printpack?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/proampac?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/scholle-corporation?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/schur-packaging-systems-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/sealed-air-corporation?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/sealstrip?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/selig-group?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/soojoung-corporation?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/spartech?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/sudpack-verpackungen-gmbh-cokg?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/taghleef-industries-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/taisei-lamick-usa?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/takigawa-corporation?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/tc-transcontinental-packaging?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/teinnovations-llc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/tekniplex-consumer-products?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/tekniplex-healthcare?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/tg-packaging-solutions-llc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/toray-plastics-america-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/totai-america-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/unified-flex-packaging-technologies?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/veritiv?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/volm-companies-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/winpak-lane-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/wj-packaging-solutions-corp?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/zacros-america-inc?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/zip-pak-an-itw-company?parent-category=materials-containers-and-consumables%2Fflexible-packaging',
 'https://www.prosource.org/company/algus-packaging?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/amcor-rigid-packaging?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/amcor-rigid-packaging?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/anchor-packaging?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/aripack?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/be-green-packaging?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/chubby-gorilla-inc?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/darifill-inc?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/double-h-plastics-inc?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/dure-co-ltd?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/elemental-container-inc?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/idemitsu-unitech-co-ltd?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/ipl-inc?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/klockner-pentaplast?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/mercury-plastics-inc?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/orbis-corporation?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/packline-usa?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/placon?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/plastic-ingenuity?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/plastipak-packaging-inc?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/point-five-packaging-llc?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/polipa-north-america?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/polytainers-inc?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/preform-solutions-inc?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/printpack?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/priority-plastics?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/rexfab-corp?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/scholle-corporation?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/sonoco?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/spartech?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/tekniplex-consumer-products?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/tripack-llc?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/visstun?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/winpak-lane-inc?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/zacros-america-inc?parent-category=materials-containers-and-consumables%2Fcontainers',
 'https://www.prosource.org/company/amcor-flexibles-north-america?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/amcor-rigid-packaging?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/aptar-food-beverage?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/bedford-industries-inc?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/cheer-pack-north-america?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/closure-systems-international-inc?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/darifill-inc?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/fres-co-system-usa-inc?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/idemitsu-unitech-co-ltd?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/kwik-lok-corporation?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/mrp-solutions?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/polipa-north-america?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/poly-clip-system-corp?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/polytainers-inc?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/proampac?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/scholle-corporation?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/silgan-equipment-company?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/tekniplex-consumer-products?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/visstun?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/volm-companies-inc?parent-category=materials-containers-and-consumables%2Fclosures-lids-and-dispensing',
 'https://www.prosource.org/company/3m?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/adhesive-products-inc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/amcor-flexibles-north-america?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/armor-usa-inc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/astro-packaging?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/bestpack-packaging-systems?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/bostik-inc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/brown-adhesives-and-equipment?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/citronix-inc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/clysar-llc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/colquimica-adhesives?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/crown-packaging-corp?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/dae-eun-smarpack?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/ebs-ink-jet-systems-usa?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/felins-inc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/gem-gravure-co-inc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/henkel-corporation?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/hsausa?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/impackt-packaging-solutions?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/industrias-tuk-sa-de-cv-hystik-inc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/inkjet-inc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/ipg-intertape-polymer-group?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/jowat-corporation?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/kao-collins-inc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/malpack-stretch-film?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/mr-machine-knives-ltd-mrmk?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/navilux-sa-de-cv?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/packline-usa?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/peacock-products?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/potdevin-machine?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/shorr-packaging?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/shurtape-technologies?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/signode?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/smith-corona?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/squid-ink-manufacturing?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/strapack-inc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/takigawa-corporation?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/tape-printers-inc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/tc-transcontinental-packaging?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/technical-adhesives-limited?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/tg-packaging-solutions-llc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/tgw-international?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/the-reynolds-company?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/veritiv?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/vibac-americas?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/videojet-technologies-inc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/york-saw-and-knife-co-inc?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/zhejiang-zhongcheng-packing-material-co-ltd?parent-category=materials-containers-and-consumables%2Fconsumables',
 'https://www.prosource.org/company/accurate-box-company?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/crown-packaging-corp?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/ds-smith?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/edibel-usa-packaging-solutions-inc?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/elopak-inc?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/emirates-printing-press?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/georgia-pacific-corrugated?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/graphic-packaging-international?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/international-paper?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/metsa-board-americas?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/orora-packaging-solutions?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/packaging-corp-of-america?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/pactiv-evergreen?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/romanow-inc?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/shafiis-inc-dba-tigerpress?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/sonoco?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/tc-transcontinental-packaging?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/tetra-pak-inc?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/veritiv?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/volm-companies-inc?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/westrock?parent-category=materials-containers-and-consumables%2Fpaperboard-and-corrugated',
 'https://www.prosource.org/company/amcor-flexibles-north-america?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/amcor-rigid-packaging?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/american-fuji-seal-inc?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/chicago-tag-and-label-inc?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/colormasters-llc?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/dcf-mexicana-sa-de-cv?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/fox-iv-technologies-inc?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/herma-us-inc?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/kdv-label-llc?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/kolinahr-systems?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/kwik-lok-corporation?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/multi-color-corporation?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/osio-international-inc?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/smith-corona?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/specialty-printing?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/upm-raflatac?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/weber-packaging-solutions?parent-category=materials-containers-and-consumables%2Flabels-and-leaflets',
 'https://www.prosource.org/company/airwave-packaging-llc?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/allstrap-steel-and-poly-strapping-systems-llc?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/bubble-paper?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/edibel-usa-packaging-solutions-inc?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/efp-llc?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/fromm-packaging-systems?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/international-dunnage?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/jadex?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/orbis-corporation?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/packaging-corp-of-america?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/pregis-llc?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/sealed-air-corporation?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/signode?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/sonoco?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/trienda?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/veritiv?parent-category=materials-containers-and-consumables%2Fprotective-and-transport-packaging',
 'https://www.prosource.org/company/a-r-arena-products-inc?parent-category=materials-containers-and-consumables%2Fbulk-packaging',
 'https://www.prosource.org/company/decade-products-llc?parent-category=materials-containers-and-consumables%2Fbulk-packaging',
 'https://www.prosource.org/company/fres-co-system-usa-inc?parent-category=materials-containers-and-consumables%2Fbulk-packaging',
 'https://www.prosource.org/company/georg-utz-inc?parent-category=materials-containers-and-consumables%2Fbulk-packaging',
 'https://www.prosource.org/company/international-paper?parent-category=materials-containers-and-consumables%2Fbulk-packaging',
 'https://www.prosource.org/company/ipl-inc?parent-category=materials-containers-and-consumables%2Fbulk-packaging',
 'https://www.prosource.org/company/mac-automation-concepts?parent-category=materials-containers-and-consumables%2Fbulk-packaging',
 'https://www.prosource.org/company/orbis-corporation?parent-category=materials-containers-and-consumables%2Fbulk-packaging',
 'https://www.prosource.org/company/proampac?parent-category=materials-containers-and-consumables%2Fbulk-packaging',
 'https://www.prosource.org/company/rehrig-pacific-company?parent-category=materials-containers-and-consumables%2Fbulk-packaging',
 'https://www.prosource.org/company/remcon-plastics-inc?parent-category=materials-containers-and-consumables%2Fbulk-packaging',
 'https://www.prosource.org/company/volm-companies-inc?parent-category=materials-containers-and-consumables%2Fbulk-packaging',
 'https://www.prosource.org/company/decker-tape-products-inc?parent-category=materials-containers-and-consumables%2Fhandles-and-carriers',
 'https://www.prosource.org/company/paktech?parent-category=materials-containers-and-consumables%2Fhandles-and-carriers',
 'https://www.prosource.org/company/roberts-polypro?parent-category=materials-containers-and-consumables%2Fhandles-and-carriers',
 'https://www.prosource.org/company/shafiis-inc-dba-tigerpress?parent-category=materials-containers-and-consumables%2Fhandles-and-carriers',
 'https://www.prosource.org/company/coim-group-north-america?parent-category=materials-containers-and-consumables%2Fresins-and-additives',
 'https://www.prosource.org/company/dow-chemical-company?parent-category=materials-containers-and-consumables%2Fresins-and-additives',
 'https://www.prosource.org/company/hb-fuller-company?parent-category=materials-containers-and-consumables%2Fresins-and-additives',
 'https://www.prosource.org/company/accurate-box-company?parent-category=materials-containers-and-consumables%2Fspecialty-display-packaging',
 'https://www.prosource.org/company/do-it-corporation?parent-category=materials-containers-and-consumables%2Fspecialty-display-packaging',
 'https://www.prosource.org/company/international-paper?parent-category=materials-containers-and-consumables%2Fspecialty-display-packaging',
 'https://www.prosource.org/company/packaging-corp-of-america?parent-category=materials-containers-and-consumables%2Fspecialty-display-packaging',
 'https://www.prosource.org/company/westrock?parent-category=materials-containers-and-consumables%2Fspecialty-display-packaging'
]

driver = webdriver.Chrome()

output_file = "./prosource/DATA_320_company_details.csv"

# Create a CSV file and write the header
with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "address", "email", "phone", "domain"])

# Function to extract data from a page
def extract_data(driver):
    try:
        # Extract company name
        company_name = driver.find_element(By.ID, "company-name").text.strip()

        # Extract address
        address = driver.find_element(By.TAG_NAME, "address").text.strip()

        # Extract email
        email_element = driver.find_element(By.XPATH, "//a[starts-with(@href, 'mailto:')]")
        email = email_element.get_attribute("href").replace("mailto:", "").strip()

        # Extract phone number
        phone_element = driver.find_element(By.XPATH, "//a[starts-with(@href, 'tel:')]")
        phone = phone_element.get_attribute("href").replace("tel:", "").strip()

        # Extract domain
        domain_element = driver.find_element(By.XPATH, "//div[contains(@class, 'text-blue-0078bd')]/a[contains(@href, 'http')]")
        domain = domain_element.get_attribute("href").strip()
        domain = cleanDomain(domain)

        return company_name, address, email, phone, domain
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None, None, None, None, None

# Loop through each URL and extract data
with open(output_file, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for url in urls:
        try:
            # Visit the URL
            driver.get(url)
            time.sleep(3)  # Wait for the page to load

            # Extract data
            company_name, address, email, phone, domain = extract_data(driver)

            # Write data to the CSV file
            if company_name:
                writer.writerow([company_name, address, email, phone, domain])
                print(f"Data extracted for {url}")
        except Exception as e:
            print(f"Error processing URL {url}: {e}")

# Close the browser
driver.quit()

print(f"Data has been saved to {output_file}")