import os
import requests
import pandas as pd
from time import sleep
from itertools import chain
from datetime import datetime
from typing import List, Iterator


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

URL = "http://api.worldbank.org/v2/country/"
DATE = datetime.today().strftime("%Y-%m-%d %H_%M")
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ISO3_PARAM = ';'.join(chain(*COUNTRIES.values()))
INDICATOR_PARAM = list(chain(*INDICATORS.values()))


def mapping(s: pd.Series, metadict: dict) -> str:
    """ Assign categories to Series' values according to dict's keys. """
    
    return ' '.join((k) for k,v in metadict.items() if s in v)


def item_level(data: List) -> Iterator:
    """ Iterate over data and yield dict containing specific fields. """
    
    for item in data:
        yield {
            "iso3": item["countryiso3code"],
            "indicator": item["indicator"]["value"],
            "id": item["indicator"]["id"],
            "year": item["date"], 
            "value": item["value"]
        }
        
def page_level(indicator: str) -> Iterator:
    """ Iterate over all pages related to specific indicator. """
    
    base_url = f"{URL}{ISO3_PARAM}/indicator/{indicator}?format=json"

    next_page = 1
    while True:
        meta, data = requests.get(f"{base_url}&page={next_page}").json()
        yield from item_level(data)
            
        num_pages, next_page = meta["pages"], next_page + 1
        if next_page > num_pages:
            break
            
        sleep(1)

def indicator_level(indicators: List) -> Iterator:
    """ Iterate over all indicators. """
    
    for indicator in indicators:
        yield from page_level(indicator) 
        

def main():
    """ Create pd.DataFrame from generator and save it. """
    df = pd.DataFrame(indicator_level(INDICATOR_PARAM))
    df["year"] = df["year"].astype(int)
    df["region"] = df["iso3"].apply(mapping, metadict=COUNTRIES)
    df["category"] = df["id"].apply(mapping, metadict=INDICATORS)
    df.loc[df["year"] >= 1991].to_excel(f"{CURRENT_DIR}/../../data/raw/dataset_{DATE}.xlsx", index=False)


if __name__ == "__main__":
    main()