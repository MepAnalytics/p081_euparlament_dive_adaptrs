"""
Step 6 (Optional): Geocode Birthplaces

Geocodes MEP birthplaces to latitude/longitude coordinates and classifies
birth regions as native, EU, or other.

Requires:
1. OpenCage API key in opencagekey.txt
2. GeoNames database in data/geonames.csv (optional, for offline geocoding)
"""

import pandas as pd
from os import path
import numpy as np
import requests
import json
import time

dir = path.dirname(__file__)

def get_coordinates_from_geonames(place_raw, geonames_df, alt_geonames_df):
    """Get coordinates from GeoNames database"""
    place = str(place_raw).lower()
    if place != "nan":
        # Remove parentheses, slashes, dashes, commas
        for sign in ["(", "/", "-", ","]:
            place = place.split(sign)[0].strip()
        
        # Try exact match first
        filter_df = geonames_df.loc[geonames_df["Name"] == place]
        if len(filter_df.index) > 0:
            return filter_df["Coordinates"].tolist()[0]
        
        # Try alternate names
        elif geonames_df["Alternate Names"].str.contains(place, na=False).any():
            alt_coordinates_df = alt_geonames_df.loc[alt_geonames_df["Alternate Names"].str.contains(place)]
            if len(alt_coordinates_df.index) > 0:
                return alt_coordinates_df["Coordinates"].tolist()[0]
    
    return np.nan

def get_classification_from_coordinates(lat, lon, elected_country, api_key):
    """Classify birth region using reverse geocoding"""
    if str(lat) == "nan":
        return np.nan
    
    coordinates = f"{lat},{lon}"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={coordinates}&key={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        response_dict = json.loads(response.content)
        response_df = pd.json_normalize(response_dict["results"])
        
        if "components.ISO_3166-1_alpha-2" in response_df.columns:
            born_country = response_df["components.ISO_3166-1_alpha-2"].values[0]
            
            eu_country_codes = [
                "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES", "FI",
                "FR", "GR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT", 
                "NL", "PL", "PT", "RO", "SE", "SI", "SK"
            ]
            
            if born_country == elected_country:
                return "native"
            elif born_country in eu_country_codes:
                return "eu"
            else:
                return "other"
    except Exception as e:
        print(f"    Warning: Geocoding error for {coordinates}: {e}")
    
    return np.nan

def main():
    """Geocode MEP birthplaces"""
    print("Geocoding MEP birthplaces...")
    
    # Check for API key
    api_key_path = path.join(dir, "..", "opencagekey.txt")
    if not path.exists(api_key_path):
        print("❌ Error: opencagekey.txt not found!")
        print("   Please create this file with your OpenCage API key")
        print("   Get a free key at: https://opencagedata.com/")
        return
    
    api_key = open(api_key_path, "r").read().strip()
    
    # Load merged data
    data_dir = path.join(dir, "..", "data")
    meps_df = pd.read_csv(path.join(data_dir, "merged.csv"), sep=";")
    
    # Check for GeoNames database
    geonames_path = path.join(data_dir, "geonames.csv")
    if path.exists(geonames_path):
        print("  Using GeoNames database for offline geocoding...")
        geonames_df = pd.read_csv(geonames_path, sep=";")
        geonames_df["Name"] = geonames_df["Name"].str.lower()
        geonames_df["Alternate Names"] = geonames_df["Alternate Names"].str.lower()
        geonames_df = geonames_df.sort_values("Population", ascending=False)
        alt_geonames_df = geonames_df.loc[geonames_df["Alternate Names"].notna()]
        
        # Geocode using GeoNames
        uncoded_df = meps_df.loc[~meps_df["born_lat"].notna()].copy()
        uncoded_df["coordinates"] = uncoded_df["born_place"].apply(
            lambda x: get_coordinates_from_geonames(x, geonames_df, alt_geonames_df)
        )
        uncoded_df = uncoded_df.loc[uncoded_df["coordinates"].notna()]
        uncoded_df[["born_lat", "born_lon"]] = uncoded_df["coordinates"].str.split(", ", expand=True)
        uncoded_df = uncoded_df.drop(["coordinates"], axis=1)
        
        # Merge back
        meps_df = pd.concat([meps_df, uncoded_df])
        meps_df = meps_df[~meps_df["identifier"].duplicated(keep="last")]
        
        print(f"  Geocoded {len(uncoded_df)} locations using GeoNames")
    else:
        print("  No GeoNames database found - skipping offline geocoding")
    
    # Classify regions using OpenCage API
    print("  Classifying birth regions using OpenCage API...")
    print("  This may take a few minutes due to API rate limits...")
    
    classifications = []
    for idx, row in meps_df.iterrows():
        if idx % 50 == 0 and idx > 0:
            print(f"    Processed {idx}/{len(meps_df)} MEPs...")
        
        classification = get_classification_from_coordinates(
            row.get("born_lat"), 
            row.get("born_lon"), 
            row["country"], 
            api_key
        )
        classifications.append(classification)
        
        # Respect API rate limits (free tier: 1 request/second)
        time.sleep(1.1)
    
    meps_df["born_region"] = classifications

    # Save output
    output_path = path.join(data_dir, "output.csv")
    meps_df.to_csv(output_path, sep=";", encoding="utf-8", index=False)
    
    native_count = len(meps_df[meps_df["born_region"] == "native"])
    eu_count = len(meps_df[meps_df["born_region"] == "eu"])
    other_count = len(meps_df[meps_df["born_region"] == "other"])
    
    print(f"✓ Successfully geocoded and classified MEPs")
    print(f"  Native: {native_count}, EU: {eu_count}, Other: {other_count}")
    print(f"✓ Saved to: {output_path}")

if __name__ == "__main__":
    main()
