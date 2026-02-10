#!/usr/bin/env python3
"""
Repository Structure Verification Script

Run this script to verify that all files are in the correct locations
before committing to GitHub.
"""

import os
from pathlib import Path

# Expected files and their locations
EXPECTED_FILES = {
    "root": [
        "README.md",
        "LICENSE",
        "INSTALL.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "PROJECT_STRUCTURE.md",
        "REPOSITORY_STRUCTURE.md",
        "PACKAGE_SUMMARY.md",
        ".gitignore",
        "Pipfile",
        "Pipfile.lock",
        "requirements.txt",
        "script.py",
        "setup_check.py",
        "opencagekey.txt.example",
    ],
    "scripts": [
        "scripts/__init__.py",
        "scripts/start.py",
        "scripts/querying.py",
        "scripts/scraper.py",
        "scripts/getwiki.py",
        "scripts/merger.py",
        "scripts/geocoding.py",
    ],
    "data": [
        "data/.gitkeep",
    ],
    "github": [
        ".github/workflows/ci.yml",
    ]
}

def check_file_exists(filepath):
    """Check if a file exists"""
    return Path(filepath).exists()

def verify_structure():
    """Verify repository structure"""
    print("=" * 70)
    print("MEP Data Collector - Repository Structure Verification")
    print("=" * 70)
    print()
    
    all_good = True
    total_files = 0
    found_files = 0
    
    # Check root files
    print("📁 ROOT DIRECTORY FILES")
    print("-" * 70)
    for filename in EXPECTED_FILES["root"]:
        total_files += 1
        exists = check_file_exists(filename)
        if exists:
            found_files += 1
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} - MISSING")
            all_good = False
    print()
    
    # Check scripts directory
    print("📁 SCRIPTS DIRECTORY")
    print("-" * 70)
    if not os.path.exists("scripts"):
        print("  ✗ scripts/ directory does not exist!")
        all_good = False
    else:
        for filepath in EXPECTED_FILES["scripts"]:
            total_files += 1
            exists = check_file_exists(filepath)
            if exists:
                found_files += 1
                print(f"  ✓ {filepath}")
            else:
                print(f"  ✗ {filepath} - MISSING")
                all_good = False
    print()
    
    # Check data directory
    print("📁 DATA DIRECTORY")
    print("-" * 70)
    if not os.path.exists("data"):
        print("  ✗ data/ directory does not exist!")
        all_good = False
    else:
        for filepath in EXPECTED_FILES["data"]:
            total_files += 1
            exists = check_file_exists(filepath)
            if exists:
                found_files += 1
                print(f"  ✓ {filepath}")
            else:
                print(f"  ✗ {filepath} - MISSING")
                all_good = False
    print()
    
    # Check GitHub workflows
    print("📁 GITHUB WORKFLOWS")
    print("-" * 70)
    if not os.path.exists(".github/workflows"):
        print("  ✗ .github/workflows/ directory does not exist!")
        all_good = False
    else:
        for filepath in EXPECTED_FILES["github"]:
            total_files += 1
            exists = check_file_exists(filepath)
            if exists:
                found_files += 1
                print(f"  ✓ {filepath}")
            else:
                print(f"  ✗ {filepath} - MISSING")
                all_good = False
    print()
    
    # Summary
    print("=" * 70)
    print(f"SUMMARY: {found_files}/{total_files} files found")
    print("=" * 70)
    
    if all_good:
        print()
        print("✅ VERIFICATION PASSED!")
        print()
        print("All files are in the correct locations.")
        print("Your repository is ready to be committed to GitHub!")
        print()
        print("Next steps:")
        print("  1. git add .")
        print("  2. git commit -m 'Initial commit: MEP Data Collector v2.0'")
        print("  3. git push origin main")
        print()
    else:
        print()
        print("❌ VERIFICATION FAILED!")
        print()
        print("Some files are missing or in wrong locations.")
        print("Please review the output above and fix the issues.")
        print()
        print("See REPOSITORY_STRUCTURE.md for correct file placement.")
        print()
        return False
    
    return True

def check_optional_files():
    """Check for optional files"""
    print("=" * 70)
    print("OPTIONAL FILES CHECK")
    print("=" * 70)
    print()
    
    optional_files = {
        "opencagekey.txt": "OpenCage API key for geocoding",
        "data/geonames.csv": "GeoNames database for offline geocoding",
        "data/disability.csv": "Custom disability data",
    }
    
    for filepath, description in optional_files.items():
        if check_file_exists(filepath):
            print(f"  ✓ {filepath} - {description}")
        else:
            print(f"  ℹ️  {filepath} - {description} (optional, not required)")
    print()

def main():
    """Main verification function"""
    # Verify we're in the right directory
    if not check_file_exists("script.py"):
        print("❌ Error: script.py not found!")
        print("Please run this script from the repository root directory.")
        return
    
    # Run verification
    structure_ok = verify_structure()
    
    # Check optional files
    check_optional_files()
    
    # Final message
    if structure_ok:
        print("=" * 70)
        print("Repository is ready for GitHub! 🎉")
        print("=" * 70)

if __name__ == "__main__":
    main()
