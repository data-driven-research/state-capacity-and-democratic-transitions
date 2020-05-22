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
ISO3_PARAM = ';'.join(chain.from_iterable(COUNTRIES.values()))
INDICATOR_PARAM = list(chain.from_iterable(INDICATORS.values()))


def invert(d):
    """ Invert dictionary. 
    
    
    >>> d = {
    ...     "cat1": ["a", "b"],
    ...     "cat2": ["c", "d"],
    ... }
    >>> invert(d)
    {'a': 'cat1', 'b': 'cat1', 'c': 'cat2', 'd': 'cat2'}
    """
    
    return {v: k for k, values in d.items() for v in values}


def extract_items(data: List) -> Iterator:
    """ Iterate over data and yield dict containing specific fields. """
    
    for item in data:
        yield {
            "iso3": item["countryiso3code"],
            "indicator": item["indicator"]["value"],
            "id": item["indicator"]["id"],
            "year": item["date"], 
            "value": item["value"]
        }
        
def get_indicator_data(indicator: str) -> Iterator:
    """ Iterate over all pages related to specific indicator. """
    
    url = f"{URL}{ISO3_PARAM}/indicator/{indicator}"
    page = 1
    while True:
        meta, data = requests.get(url, params={"page": page, "format": "json"}).json()
        yield from extract_items(data)
        page += 1
        if page > meta["pages"]:
            break
        sleep(1)

def get_dataframe(indicators: List) -> Iterator:
    """ Iterate over all indicators. """
    
    for indicator in indicators:
        yield from get_indicator_data(indicator) 
        

def main():
    """ Create pd.DataFrame from generator and save it. """
    df = pd.DataFrame(get_dataframe(INDICATOR_PARAM))
    df["year"] = df["year"].astype(int)
    df["region"] = df["iso3"].map(invert(COUNTRIES))
    df["category"] = df["id"].map(invert(INDICATORS))
    df.loc[df["year"] >= 1991].to_excel(f"{CURRENT_DIR}/../../data/raw/dataset_{DATE}.xlsx", index=False)


if __name__ == "__main__":
    main()