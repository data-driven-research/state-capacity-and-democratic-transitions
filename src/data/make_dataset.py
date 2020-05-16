import os
import requests
import pandas as pd
from time import sleep
from itertools import chain
from datetime import datetime


URL = "http://api.worldbank.org/v2/country/"
DATE = datetime.today().strftime("%Y-%m-%d %H_%M")
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

COUNTRIES = {
    "Baltic States": ["EST", "LVA", "LTU"],
    "Central Asia": ["KAZ", "KGZ", "TJK", "TKM", "UZB"],
    "Eastern Europe": ["BLR", "MDA", "UKR"],
    "Eurasia": ["RUS"],
    "Transcaucasia": ["ARM", "AZE", "GEO"]
}
INDICATORS = {
    "Infrastructure": ["EG.ELC.ACCS.RU.ZS", "IT.CEL.SETS"],
    "Medicine": ["SH.DYN.MORT", "SH.DYN.AIDS.ZS"],
    "Public Sector": ["GC.TAX.TOTL.GD.ZS", "MS.MIL.TOTL.TF.ZS"]
}


def mapping(s, metadict):
    return ' '.join((k) for k,v in metadict.items() if s in v)


def item_generator(data):
    
    for item in data:
        yield {
            "iso3": item["countryiso3code"],
            "indicator": item["indicator"]["value"],
            "id": item["indicator"]["id"],
            "year": item["date"], 
            "value": item["value"]
        }
        

def indicator_generator(indicators):
    
    _iso3 = ';'.join(chain(*COUNTRIES.values()))
    
    for indicator in indicators:
        meta = requests.get(f"{URL}{_iso3}/indicator/{indicator}?format=json").json()[0]
        sleep(1)
        
        for page in range(1, meta["pages"]+1):
            meta, data = requests.get(f"{URL}{_iso3}/indicator/{indicator}?format=json&page={page}").json()
            yield from item_generator(data)
            sleep(1)
        

def main():
    df = pd.DataFrame(indicator_generator(list(chain(*INDICATORS.values()))))
    df["year"] = df["year"].astype(int)
    df["region"] = df["iso3"].apply(mapping, metadict=COUNTRIES)
    df["category"] = df["id"].apply(mapping, metadict=INDICATORS)
    df.loc[df["year"] >= 1991].to_excel(f"{CURRENT_DIR}/../../data/raw/dataset_{DATE}.xlsx", index=False)


if __name__ == "__main__":
    main()