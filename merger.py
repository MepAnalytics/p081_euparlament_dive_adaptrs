"""
Step 5: Merge All Data Sources

Merges data from all previous steps (EP API, Parliament database, scraped profiles, 
Wikidata) into a single consolidated dataset.
"""

import pandas as pd
import numpy as np
from os import path

dir = path.dirname(__file__)

def keep_highest_degree(degree_string):
    """Keep only the highest educational degree"""
    degree_string = str(degree_string)
    if degree_string != "nan":
        degree_hierarchy = ["phd", "university", "secondary", "vocational"]
        degree_list = degree_string.split(",")
        for degree in degree_hierarchy:
            if degree in degree_list:
                return degree
    return np.nan

def main():
    """Merge all data sources into final dataset"""
    print("Merging all data sources...")
    
    # Load all dataframes
    data_dir = path.join(dir, "..", "data")
    
    print("  Loading data files...")
    start_df = pd.read_csv(path.join(data_dir, "start.csv"), sep=";")
    details_df = pd.read_csv(path.join(data_dir, "details.csv"), sep=";")
    scraped_df = pd.read_csv(path.join(data_dir, "scraped.csv"), sep=";")
    wikidata_df = pd.read_csv(path.join(data_dir, "wikidata.csv"), sep=";")
    
    # Load optional disability data if it exists
    disability_path = path.join(data_dir, "disability.csv")
    if path.exists(disability_path):
        disability_df = pd.read_csv(disability_path, sep=";")
        has_disability_data = True
        print("  Found disability.csv - including in merge")
    else:
        has_disability_data = False
        print("  No disability.csv found - skipping")

    # First merge simple ones
    print("  Merging primary data sources...")
    first_merge_df = pd.merge(start_df, details_df, on="identifier", how="left")
    second_merge_df = pd.merge(first_merge_df, scraped_df, on="identifier", how="left")

    # Prepare names to be merged on
    second_merge_df["name"] = second_merge_df["name"].str.lower().str.strip()
    wikidata_df["name"] = wikidata_df["name"].str.lower().str.strip()

    # Do the complicated fill-merges for birthplace & -date
    print("  Filling missing birth data from Wikidata...")
    
    # Birthplace
    wikidata_place_df = wikidata_df[["name", "born_place"]]
    place_missing = second_merge_df.loc[second_merge_df["born_place"].isna()]["name"].tolist()
    place_in_df = second_merge_df.loc[second_merge_df["born_place"].notna()][["name", "born_place"]]
    wikidata_place_df = wikidata_place_df.loc[wikidata_place_df["name"].isin(place_missing)]
    place_filled_df = pd.concat([place_in_df, wikidata_place_df], ignore_index=True)

    # Birth date
    wikidata_date_df = wikidata_df[["name", "born_day", "born_month", "born_year"]]
    date_missing = second_merge_df.loc[second_merge_df["born_year"].isna()]["name"].tolist()
    date_in_df = second_merge_df.loc[second_merge_df["born_year"].notna()][["name", "born_day", "born_month", "born_year"]]
    wikidata_date_df = wikidata_date_df.loc[wikidata_date_df["name"].isin(date_missing)]
    date_filled_df = pd.concat([date_in_df, wikidata_date_df], ignore_index=True)

    # Rest of Wikidata info
    wikidata_rest_df = wikidata_df[["name", "relatives", "degrees", "educated_at", "occupation"]]
    second_merge_df = second_merge_df.drop(columns=["born_day", "born_month", "born_year", "born_place"])

    # Merge everything
    print("  Merging Wikidata biographical information...")
    third_merge_df = pd.merge(second_merge_df, place_filled_df, on="name", how="left")
    fourth_merge_df = pd.merge(third_merge_df, date_filled_df, on="name", how="left")
    
    if has_disability_data:
        fifth_merge_df = pd.merge(fourth_merge_df, disability_df, on="identifier", how="left")
    else:
        fifth_merge_df = fourth_merge_df
    
    merged_df = pd.merge(fifth_merge_df, wikidata_rest_df, on="name", how="left")

    # Merge degrees and occupation columns
    print("  Consolidating education and occupation data...")
    merged_df = merged_df.fillna("")
    merged_df["degrees"] = merged_df.apply(
        lambda row: ",".join(set(row["degrees_x"].split(",") + row["degrees_y"].split(","))), 
        axis=1
    )
    merged_df["occupation"] = merged_df.apply(
        lambda row: ",".join(set(row["occupation_x"].split(",") + row["occupation_y"].split(","))), 
        axis=1
    )
    
    # Clean up merged strings
    merged_df["degrees"] = merged_df["degrees"].str.strip(",").str.replace(",,", ",")
    merged_df["occupation"] = merged_df["occupation"].str.strip(",").str.replace(",,", ",")
    merged_df = merged_df.replace("", np.nan)

    # Only keep the highest degree
    merged_df["degrees"] = merged_df["degrees"].apply(keep_highest_degree)
    merged_df = merged_df.rename(columns={"degrees": "highest_degree"})

    # Drop unwanted columns
    columns_to_drop = ["id", "type", "sortLabel", "officialFamilyName", "officialGivenName",
                      "degrees_x", "degrees_y", "occupation_x", "occupation_y"]
    columns_to_drop = [col for col in columns_to_drop if col in merged_df.columns]
    merged_df = merged_df.drop(columns=columns_to_drop)

    # Drop duplicate rows
    merged_df = merged_df[~merged_df["identifier"].duplicated()]

    # Convert dates to int
    for column in ["born_day", "born_month", "born_year"]:
        merged_df[column] = merged_df[column].fillna(0).astype(int)
        merged_df[column] = merged_df[column].replace(0, np.nan)

    # Save final output
    output_path = path.join(data_dir, "output.csv")
    merged_df.to_csv(output_path, sep=";", encoding="utf-8", index=False)
    
    print(f"✓ Successfully merged all data sources")
    print(f"✓ Final dataset contains {len(merged_df)} MEPs with {len(merged_df.columns)} attributes")
    print(f"✓ Saved to: {output_path}")

if __name__ == "__main__":
    main()
