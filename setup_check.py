"""
Setup and Environment Validation Script

Run this script to check if your environment is properly configured
for the MEP Data Collector pipeline.
"""

import sys
from os import path, makedirs

def check_python_version():
    """Check if Python version is 3.11 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"❌ Python 3.11+ required. You have {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'requests': 'HTTP library',
        'pandas': 'Data manipulation',
        'numpy': 'Numerical operations',
        'bs4': 'BeautifulSoup web scraping',
        'json': 'JSON parsing (built-in)',
    }
    
    missing = []
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {package:15s} - {description}")
        except ImportError:
            print(f"❌ {package:15s} - {description} (NOT INSTALLED)")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("   Install with: pip install -r requirements.txt")
        print("   Or with pipenv: pipenv install")
        return False
    return True

def check_directory_structure():
    """Check if required directories exist"""
    current_dir = path.dirname(__file__)
    
    # Check for scripts directory
    scripts_dir = path.join(current_dir, "scripts")
    if not path.exists(scripts_dir):
        print(f"❌ Scripts directory not found: {scripts_dir}")
        return False
    print(f"✓ Scripts directory exists")
    
    # Check for individual scripts
    required_scripts = ['start.py', 'querying.py', 'scraper.py', 'getwiki.py', 'merger.py']
    for script in required_scripts:
        script_path = path.join(scripts_dir, script)
        if not path.exists(script_path):
            print(f"❌ Missing script: {script}")
            return False
    print(f"✓ All required scripts present")
    
    # Create data directory if it doesn't exist
    data_dir = path.join(current_dir, "data")
    if not path.exists(data_dir):
        makedirs(data_dir)
        print(f"✓ Created data directory: {data_dir}")
    else:
        print(f"✓ Data directory exists")
    
    return True

def check_optional_files():
    """Check for optional configuration files"""
    current_dir = path.dirname(__file__)
    
    # Check for OpenCage API key
    api_key_path = path.join(current_dir, "opencagekey.txt")
    if path.exists(api_key_path):
        print("✓ OpenCage API key found (geocoding enabled)")
    else:
        print("ℹ️  OpenCage API key not found (geocoding disabled)")
        print("   To enable geocoding:")
        print("   1. Get a free key from https://opencagedata.com/")
        print("   2. Save it to opencagekey.txt")
    
    # Check for GeoNames database
    data_dir = path.join(current_dir, "data")
    geonames_path = path.join(data_dir, "geonames.csv")
    if path.exists(geonames_path):
        print("✓ GeoNames database found (offline geocoding available)")
    else:
        print("ℹ️  GeoNames database not found (online geocoding only)")
    
    # Check for disability data
    disability_path = path.join(data_dir, "disability.csv")
    if path.exists(disability_path):
        print("✓ Disability data found")
    else:
        print("ℹ️  Disability data not found (optional)")

def main():
    """Run all validation checks"""
    print("=" * 60)
    print("MEP Data Collector - Setup Validation")
    print("=" * 60)
    print()
    
    print("Checking Python version...")
    python_ok = check_python_version()
    print()
    
    print("Checking dependencies...")
    deps_ok = check_dependencies()
    print()
    
    print("Checking directory structure...")
    dirs_ok = check_directory_structure()
    print()
    
    print("Checking optional files...")
    check_optional_files()
    print()
    
    print("=" * 60)
    if python_ok and deps_ok and dirs_ok:
        print("✓ Setup validation PASSED")
        print("=" * 60)
        print()
        print("You're ready to run the data collection pipeline!")
        print("Run: python script.py")
        print()
    else:
        print("❌ Setup validation FAILED")
        print("=" * 60)
        print()
        print("Please fix the issues above before running the pipeline.")
        print()

if __name__ == "__main__":
    main()
