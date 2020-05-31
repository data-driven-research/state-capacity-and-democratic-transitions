import pandas as pd


def min_max_normalization(v, reverse=False):
    """ Apply min-max normalization per year & indicator. """
    
    formula = (v - v.min()) / (v.max() - v.min())
    if reverse:
        return 1 - formula
    else:
        return formula

    
def case_selection(df):
    """ Filter relevant cases. """
    
    case_1 = (df["iso3"].eq("SRB") & df["year"].eq(2000))
    case_2 = (df["iso3"].eq("GEO") & df["year"].eq(2003))
    case_3 = (df["iso3"].eq("UKR") & df["year"].eq(2004))
    case_4 = (df["iso3"].eq("KGZ") & df["year"].eq(2005))
    case_5 = (df["iso3"].eq("MDA") & df["year"].eq(2009))
    case_6 = (df["iso3"].eq("KGZ") & df["year"].eq(2010))
    case_7 = (df["iso3"].eq("UKR") & df["year"].eq(2014))
    case_8 = (df["iso3"].eq("ARM") & df["year"].eq(2018))
    
    selected = df.loc[
        case_1 | case_2 | case_3 | case_4 | 
        case_5 | case_6 | case_7 | case_8
    ].copy()
    
    return selected