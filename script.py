"""
MEP Data Collector - Main Orchestration Script

This script runs the complete data collection pipeline for Members of the European Parliament.
It sequentially executes all data collection and processing scripts.
"""

from os import path
import subprocess
import sys

dir = path.dirname(__file__)

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    
    script_path = path.join(dir, "scripts", f"{script_name}.py")
    result = subprocess.call([sys.executable, script_path])
    
    if result != 0:
        print(f"\n❌ Error running {script_name}.py (exit code: {result})")
        print(f"Pipeline stopped. Please check the error above.")
        sys.exit(1)
    else:
        print(f"✓ {description} completed successfully")
    
    return result

def main():
    """Execute the complete MEP data collection pipeline"""
    print("\n" + "="*60)
    print("MEP DATA COLLECTION PIPELINE")
    print("European Parliament - 10th Term (2024-2029)")
    print("="*60)
    
    # Step 1: Download initial list
    run_script("start", "Step 1/5: Downloading initial MEP list from EP API")
    
    # Step 2: Query Parliament database
    run_script("querying", "Step 2/5: Querying Parliament database for details")
    
    # Step 3: Scrape profiles
    run_script("scraper", "Step 3/5: Scraping MEP profile pages")
    
    # Step 4: Query Wikidata
    run_script("getwiki", "Step 4/5: Querying Wikidata for biographical data")
    
    # Step 5: Merge all data
    run_script("merger", "Step 5/5: Merging all data sources")
    
    # Optional Step 6: Geocoding (commented out by default)
    # Uncomment the following lines to enable geocoding
    # print("\nNote: Geocoding requires an OpenCage API key in opencagekey.txt")
    # run_script("geocoding", "Step 6/6 (Optional): Geocoding birthplaces")
    
    print("\n" + "="*60)
    print("✓ PIPELINE COMPLETED SUCCESSFULLY")
    print("="*60)
    print(f"\nOutput file: {path.join(dir, 'data', 'output.csv')}")
    print("\nTo enable geocoding:")
    print("1. Get a free API key from https://opencagedata.com/")
    print("2. Save it to opencagekey.txt in the project root")
    print("3. Uncomment the geocoding lines in this script")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPipeline interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
