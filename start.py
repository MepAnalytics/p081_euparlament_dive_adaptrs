"""
Step 1: Download Initial MEP List

Fetches the current list of MEPs from the European Parliament API.
Downloads basic information including names, countries, and political groups.
"""

import requests
import json
import pandas as pd
from os import path, makedirs

dir = path.dirname(__file__)

def main():
    """Fetch current MEPs from European Parliament API"""
    print("Fetching MEP list from European Parliament API...")
    
    try:
        # Query the EP API for current MEPs
        query_result = requests.get(
            "https://data.europarl.europa.eu/api/v1/meps/show-current",
            headers={"Accept": "application/ld+json"}
        )
        query_result.raise_for_status()
        
        # Parse JSON response
        meps_dict = json.loads(query_result.content)
        meps_df = pd.json_normalize(meps_dict["data"])
        
        # Rename columns for clarity
        meps_df = meps_df.rename(columns={
            "label": "name",
            "api:country-of-representation": "country",
            "api:political-group": "group"
        })
        
        # Create data directory if it doesn't exist
        data_directory = path.join(dir, "..", "data")
        if not path.exists(data_directory):
            makedirs(data_directory)
            print(f"Created data directory: {data_directory}")
        
        # Save to CSV
        output_path = path.join(dir, "..", "data", "start.csv")
        meps_df.to_csv(output_path, sep=";", encoding="utf-8", index=False)
        
        print(f"✓ Successfully downloaded {len(meps_df)} MEPs")
        print(f"✓ Saved to: {output_path}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data from EP API: {e}")
        raise
    except Exception as e:
        print(f"❌ Error processing MEP data: {e}")
        raise

if __name__ == "__main__":
    main()
