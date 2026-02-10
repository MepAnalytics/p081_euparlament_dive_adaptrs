"""
Step 2: Query Parliament Database

Queries the European Parliament RDF database for additional MEP details,
specifically gender information.
"""

import requests
import json
import pandas as pd
from os import path
import time

dir = path.dirname(__file__)

def query_gender(identifier):
    """Query Parliament database for MEP gender"""
    try:
        url = f"https://data.europarl.europa.eu/person/{identifier}"
        response = requests.get(url, headers={"Accept": "application/ld+json"})
        response.raise_for_status()
        
        mep_dict = json.loads(response.content)
        mep_df = pd.json_normalize(mep_dict["@graph"])
        
        # Extract gender from RDF data
        if "hasGender" in mep_df.columns:
            gender_uri = str(mep_df["hasGender"].dropna().values[0])
            gender = gender_uri.split("/")[-1]
            return gender
        else:
            return None
            
    except Exception as e:
        print(f"  Warning: Could not fetch gender for {identifier}: {e}")
        return None

def main():
    """Query Parliament database for all MEPs"""
    print("Querying Parliament database for MEP details...")
    
    # Load initial MEP list
    input_path = path.join(dir, "..", "data", "start.csv")
    meps_df = pd.read_csv(input_path, sep=";")
    
    print(f"Processing {len(meps_df)} MEPs...")
    
    # Get identifiers
    mep_identifiers = meps_df["identifier"].tolist()
    
    # Create dataframe for details
    mep_details_df = pd.DataFrame(mep_identifiers, columns=["identifier"])
    
    # Query each MEP (with progress indicator)
    genders = []
    for i, identifier in enumerate(mep_identifiers, 1):
        if i % 50 == 0:
            print(f"  Processed {i}/{len(mep_identifiers)} MEPs...")
        
        gender = query_gender(identifier)
        genders.append(gender)
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.1)
    
    mep_details_df["gender"] = genders
    
    # Save results
    output_path = path.join(dir, "..", "data", "details.csv")
    mep_details_df.to_csv(output_path, sep=";", encoding="utf-8", index=False)
    
    print(f"✓ Successfully queried {len(mep_details_df)} MEPs")
    print(f"✓ Saved to: {output_path}")

if __name__ == "__main__":
    main()
