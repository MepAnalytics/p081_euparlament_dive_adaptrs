"""
Step 3: Scrape MEP Profile Pages

Scrapes biographical information from MEP profile pages on europarl.europa.eu
including birth dates, birthplaces, education, career history, and memberships.
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
from os import path
import time

dir = path.dirname(__file__)

# Define dictionaries for degrees and careers
degree_dict = {
    "secondary": ["secondary", "gymnasium", "vocat", "apprentice", "high school"],
    "university": ["university", "college", "degree", "diplom", "bachelor", "master", "graduate", "studied", "bsc", "msc", " ba ", " ma "],
    "phd": ["doctor", "postgraduate", "phd", "ph.d"]
}

career_dict = {
    "farmer": ["farmer"],
    "lawyer": ["lawyer", "legal", "judge"],
    "media": ["journalist", "reporter", "editor", "newsroom", "newspaper", "press", "advertis", "public relations"],
    "politician": ["mep", "party", "parliament", "policy officer", "mayor", "minister", "councillor"],
    "official": ["official", "ministry", "public service", "diplomat"],
    "doctor": ["doctor"],
    "teacher": ["teacher", "instructor", "lecturer"],
    "engineer": ["engineer"],
    "researcher": ["researcher", "expert", "professor"],
    "manager": ["manager", "director", "chairman", "chairwoman", "chairperson", "head of", "member of the board", "board member", "chair of the"],
    "consultant": ["consultant"],
    "labourer": ["welder"]
}

def scrape_mep(url):
    """Scrape biographical data from a single MEP profile page"""
    mep_dict = {}

    try:
        # Scrape main profile page
        response = requests.get(url + "/home")
        response.raise_for_status()
        html = response.text
        doc = BeautifulSoup(html, "html.parser")

        # Birth date
        try:
            birthdate = doc.find("time", {"class": "sln-birth-date"})
            birthdate = birthdate.text.strip().split("-")
            mep_dict["born_day"] = int(birthdate[0])
            mep_dict["born_month"] = int(birthdate[1])
            mep_dict["born_year"] = int(birthdate[2])
        except:
            mep_dict["born_day"] = np.nan
            mep_dict["born_month"] = np.nan
            mep_dict["born_year"] = np.nan

        # Birth place
        try:
            birthplace = doc.find("span", {"class": "sln-birth-place"})
            mep_dict["born_place"] = birthplace.text
        except:
            mep_dict["born_place"] = np.nan

        # Memberships (committees, delegations, etc.)
        mep_dict["memberships"] = np.nan
        status_list = doc.findAll("div", {"class": "erpl_meps-status"})
        for status in status_list:
            badges = status.findAll("a", {"class": "erpl_badge"})
            for badge in badges:
                if not pd.isna(mep_dict["memberships"]):
                    mep_dict["memberships"] += ","
                    mep_dict["memberships"] += badge.text
                else:
                    mep_dict["memberships"] = badge.text

        # Scrape CV page
        headers = {"Accept-Language": "en;q=1.0"}
        response = requests.get(url + "/cv", headers=headers)
        response.raise_for_status()
        html = response.text
        doc = BeautifulSoup(html, "html.parser")
                
        mep_dict["degrees"] = np.nan
        mep_dict["occupation"] = np.nan

        activity_list = doc.findAll("div", {"class": "erpl_meps-activity"})
        for activity in activity_list:
            category = activity.find("h4", {"class": "erpl_title-h4"}).text
            activity_content = activity.find("ul", {"class": "pl-2"})
            
            if category == "Education (qualifications and diplomas)":
                education_str = activity_content.text.strip().lower()
                for key in degree_dict.keys(): 
                    add = False
                    for word in degree_dict[key]:
                        if word in education_str:
                            add = True
                    if add:
                        if not pd.isna(mep_dict["degrees"]):
                            mep_dict["degrees"] += "," + key
                        else:
                            mep_dict["degrees"] = key
                            
            if category == "Professional career":
                career_str = activity_content.text.strip().lower()
                for key in career_dict.keys(): 
                    add = False
                    for word in career_dict[key]:
                        if word in career_str:
                            add = True
                    if add:
                        if not pd.isna(mep_dict["occupation"]):
                            mep_dict["occupation"] += "," + key
                        else:
                            mep_dict["occupation"] = key

    except Exception as e:
        print(f"    Warning: Error scraping {url}: {e}")

    return mep_dict

def main():
    """Scrape all MEP profile pages"""
    print("Scraping MEP profile pages...")
    
    # Load initial MEP list
    input_path = path.join(dir, "..", "data", "start.csv")
    meps_df = pd.read_csv(input_path, sep=";")
    
    # Construct URLs for MEP profile pages
    mep_urls = []
    for idx, row in meps_df.iterrows():
        identifier = str(row["identifier"])
        given_name = str(row["givenName"])
        family_name = str(row["familyName"])
        url = f"https://www.europarl.europa.eu/meps/en/{identifier}/{given_name}_{family_name}"
        mep_urls.append([identifier, url])

    print(f"Scraping {len(mep_urls)} MEP profiles...")
    print("This may take several minutes...")
    
    # Scrape each profile
    dict_of_dicts = {}
    for i, (identifier, url) in enumerate(mep_urls, 1):
        if i % 50 == 0:
            print(f"  Processed {i}/{len(mep_urls)} profiles...")
        
        dict_of_dicts[identifier] = scrape_mep(url)
        
        # Delay to be respectful to the server
        time.sleep(0.5)
    
    # Convert to dataframe
    scraped_df = pd.DataFrame.from_dict(dict_of_dicts).transpose()
    scraped_df = scraped_df.reset_index().rename(columns={"index": "identifier"})
    
    # Save results
    output_path = path.join(dir, "..", "data", "scraped.csv")
    scraped_df.to_csv(output_path, sep=";", encoding="utf-8", index=False)
    
    print(f"✓ Successfully scraped {len(scraped_df)} MEP profiles")
    print(f"✓ Saved to: {output_path}")

if __name__ == "__main__":
    main()
