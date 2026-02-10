"""
Step 4: Query Wikidata

Queries Wikidata via SPARQL for enriched biographical information about MEPs
including family relations, education, occupations, and birthplace data.

Updated for 10th European Parliament (2024-2029)
"""

import pandas as pd
import requests
import json
from os import path
import numpy as np

dir = path.dirname(__file__)

# Degree & occupation dictionaries
degree_dict = {
    "secondary": ["secondary", "gymnasium", "vocat", "apprentice", "high school"],
    "university": ["master", "bachelor", "diplom", "magister", "laurea", "degree", "law"],
    "phd": ["doctor", "habilitation", "professor", "candidat"]
}

occupation_dict = {
    "politician": ["politician", "member of the european parliament"],
    "lawyer": ["lawyer", "judge", "jurist", "justiciar", "legal", "barrister", "officer of the court"],
    "engineer": ["engineer"],
    "farmer": ["farmer", "farm operator", "rancher", "vigneron"],
    "consultant": ["consultant"],
    "researcher": ["researcher", "academic", "professor", "scientist", "historian", "sociologist", "chemist", 
                   "physicist", "agronomist", "philologist", "scientist", "mathematician",
                   "pedagogue", "economist", "ecologist", "geographer", "philosopher", "professor", "academic"],
    "media": ["presenter", "journalist", "press", "blogger", "correspondent"],
    "activist": ["environmentalist", "activist", "dissident", "humanitarian"],
    "athlete": ["athlete", "football", "hurler", "swimmer", "athletics", "badminton player"],
    "official": ["civil servant", "minister", "official", "eurocrat", "magistrate", "diplomat"],
    "teacher": ["teacher"],
    "actor": ["actor"],
    "manager": ["manager", "executive"],
    "businessperson": ["businessperson", "entrepeneur", "shopkeeper", "self-employment"],
    "doctor": ["doctor", "nurse", "physician", "veterinarian", "pharmacist", "surgeon", "psychiatrist", "psychologist"],
}

def categorise(entry, category_dict):
    """Categorize text entries based on keyword matching"""
    if not entry:
        return np.nan
    new_entry = []
    entry_list = entry.split(",")
    for entry_part in entry_list:
        entry_part = entry_part.lower().strip()
        found = False
        for category in category_dict.keys():
            for keyword in category_dict[category]:
                if keyword in entry_part:
                    found = True
                    if category not in new_entry:
                        new_entry.append(category)
        if not found:
            new_entry.append(entry_part)
    return ",".join(new_entry)

def main():
    """Query Wikidata for MEP biographical information"""
    print("Querying Wikidata for MEP biographical data...")
    print("This may take a minute or two...")
    
    # SPARQL query for 10th European Parliament (2024-2029)
    # Entity: wd:Q75984568
    query = '''SELECT ?mep ?mepLabel ?fatherLabel ?motherLabel ?birthdateLabel ?birthplace ?birthplaceLabel ?relativeLabel ?degreeLabel ?educatedatLabel ?occupationLabel
WHERE { 
  ?mep p:P39 ?position. 
  ?position (ps:P39/(wdt:P279*)) wd:Q27169. 
  ?position pq:P2937 ?term. 
  FILTER(?term = wd:Q75984568).  
  OPTIONAL{ ?mep wdt:P22 ?father. }
  OPTIONAL{ ?mep wdt:P25 ?mother. }
  OPTIONAL{ ?mep wdt:P569 ?birthdate. }
  OPTIONAL{ ?mep wdt:P19 ?birthplace. }
  OPTIONAL{ ?mep wdt:P1038 ?relative. }
  OPTIONAL{ ?mep wdt:P512 ?degree. }
  OPTIONAL{ ?mep wdt:P69 ?educatedat. }
  OPTIONAL{ ?mep wdt:P106 ?occupation. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}'''
    
    try:
        # Query Wikidata SPARQL endpoint
        wikidata_url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
        query_result = requests.get(wikidata_url, params={"query": query, "format": "json"})
        query_result.raise_for_status()
        
        # Parse results
        meps_dict = json.loads(query_result.content)
        meps_df = pd.json_normalize(meps_dict["results"]["bindings"])
        meps_df = meps_df.fillna("")
        
        print(f"  Retrieved data for {len(meps_df)} MEP records from Wikidata")
        
        # Group rows for MEPs with multiple relatives, degrees, educations or occupations
        merged_meps_df = meps_df.groupby([
            "mep.value", "mepLabel.value", "fatherLabel.value", "motherLabel.value", 
            "birthdateLabel.value", "birthplaceLabel.value", "birthplace.value"
        ]).agg({
            "relativeLabel.value": lambda x: ",".join(list(set(x.astype(str)))),
            "degreeLabel.value": lambda x: ",".join(list(set(x.astype(str)))),
            "educatedatLabel.value": lambda x: ",".join(list(set(x.astype(str)))),
            "occupationLabel.value": lambda x: ",".join(list(set(x.astype(str)))),
        }).reset_index()

        # Rename columns
        merged_meps_df = merged_meps_df.rename(columns={
            "mepLabel.value": "name",
            "fatherLabel.value": "father",
            "motherLabel.value": "mother",
            "birthdateLabel.value": "born_date",
            "birthplaceLabel.value": "born_place",
            "relativeLabel.value": "relatives",
            "degreeLabel.value": "degrees",
            "educatedatLabel.value": "educated_at",
            "occupationLabel.value": "occupation",
            "birthplace.value": "birthplace_link"
        })

        # Split born_date column
        merged_meps_df["born_day"] = merged_meps_df["born_date"].str.split("-").str.get(2).str[:2]
        merged_meps_df["born_month"] = merged_meps_df["born_date"].str.split("-").str.get(1)
        merged_meps_df["born_year"] = merged_meps_df["born_date"].str.split("-").str.get(0)
        merged_meps_df = merged_meps_df.drop(columns=["mep.value", "born_date"])

        # Group father, mother and relative columns
        def join_strings(row, columns):
            return ",".join(value for column, value in zip(merged_meps_df.columns, row) 
                          if column in columns and pd.notna(value) and value != "")
        
        merged_meps_df["relatives"] = merged_meps_df.apply(
            lambda row: join_strings(row, ["father", "mother", "relatives"]), axis=1
        )

        # Categorise degrees & occupations
        merged_meps_df["degrees"] = merged_meps_df["degrees"].apply(lambda x: categorise(x, degree_dict))
        merged_meps_df["occupation"] = merged_meps_df["occupation"].apply(lambda x: categorise(x, occupation_dict))

        # Manual name overrides if Wikidata name not identical to Parliament database
        # These may need updating for the 10th EP
        merged_meps_df["name"] = merged_meps_df["name"].replace({
            "Rosa Estaràs": "Rosa ESTARÀS FERRAGUT",
            "Tomasz Poręba": "Tomasz Piotr PORĘBA",
            "Carles Puigdemont": "Carles Puigdemont i Casamajó",
            "Soraya Rodríguez": "María Soraya RODRÍGUEZ RAMOS",
            "Petros S. Kokkalis": "Petros KOKKALIS",
            "Graça Carvalho": "Maria da Graça CARVALHO",
            "Diana Riba Giner": "Diana RIBA I GINER",
            "Eva-Maria Poptcheva": "Eva Maria Poptcheva",
            "Yannis Lagos": "Ioannis Lagos",
            "Cristian Terheș": "Cristian TERHEŞ"
        })

        # Save
        output_path = path.join(dir, "..", "data", "wikidata.csv")
        merged_meps_df.to_csv(output_path, sep=";", encoding="utf-8", index=False)
        
        print(f"✓ Successfully processed {len(merged_meps_df)} unique MEPs from Wikidata")
        print(f"✓ Saved to: {output_path}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error querying Wikidata: {e}")
        raise
    except Exception as e:
        print(f"❌ Error processing Wikidata results: {e}")
        raise

if __name__ == "__main__":
    main()
