# Repository File Structure Guide

This document shows exactly where each file should be placed in your GitHub repository.

## Complete Directory Tree

```
mep-data-collector/                 # Root directory
│
├── README.md                       # Main documentation (ROOT)
├── LICENSE                         # MIT License (ROOT)
├── INSTALL.md                      # Installation guide (ROOT)
├── CONTRIBUTING.md                 # Contribution guidelines (ROOT)
├── CHANGELOG.md                    # Version history (ROOT)
├── PROJECT_STRUCTURE.md            # Project overview (ROOT)
├── .gitignore                      # Git ignore rules (ROOT)
├── Pipfile                         # Pipenv config (ROOT)
├── Pipfile.lock                    # Locked dependencies (ROOT)
├── requirements.txt                # Pip dependencies (ROOT)
├── script.py                       # Main orchestrator (ROOT)
├── setup_check.py                  # Validation script (ROOT)
├── opencagekey.txt.example         # API key template (ROOT)
│
├── scripts/                        # Scripts directory
│   ├── __init__.py                # Package initializer
│   ├── start.py                   # Step 1: Fetch MEP list
│   ├── querying.py                # Step 2: Query Parliament DB
│   ├── scraper.py                 # Step 3: Scrape profiles
│   ├── getwiki.py                 # Step 4: Query Wikidata ⭐ UPDATED
│   ├── merger.py                  # Step 5: Merge datasets
│   └── geocoding.py               # Step 6: Geocode (optional)
│
├── data/                           # Data directory
│   └── .gitkeep                   # Keeps empty dir in git
│
└── .github/                        # GitHub config directory
    └── workflows/                  # GitHub Actions workflows
        └── ci.yml                  # CI/CD configuration

```

## File Placement Checklist

### Root Directory Files (11 files)
Place these files directly in the repository root:

- [ ] README.md
- [ ] LICENSE
- [ ] INSTALL.md
- [ ] CONTRIBUTING.md
- [ ] CHANGELOG.md
- [ ] PROJECT_STRUCTURE.md
- [ ] .gitignore
- [ ] Pipfile
- [ ] Pipfile.lock
- [ ] requirements.txt
- [ ] script.py
- [ ] setup_check.py
- [ ] opencagekey.txt.example

### scripts/ Directory (7 files)
Create a `scripts/` folder and place these files inside:

- [ ] scripts/__init__.py
- [ ] scripts/start.py
- [ ] scripts/querying.py
- [ ] scripts/scraper.py
- [ ] scripts/getwiki.py ⭐ **Contains the 10th EP update**
- [ ] scripts/merger.py
- [ ] scripts/geocoding.py

### data/ Directory (1 file)
Create a `data/` folder and place this file inside:

- [ ] data/.gitkeep

**Note**: CSV files will be auto-generated here when you run the pipeline.

### .github/workflows/ Directory (1 file)
Create `.github/workflows/` nested folders and place this file inside:

- [ ] .github/workflows/ci.yml

## Setup Instructions

### Option 1: Manual Setup

1. **Create the repository** on GitHub
2. **Clone it locally**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/mep-data-collector.git
   cd mep-data-collector
   ```

3. **Create directories**:
   ```bash
   mkdir scripts
   mkdir data
   mkdir -p .github/workflows
   ```

4. **Add all files** to their respective locations according to the tree above

5. **Commit and push**:
   ```bash
   git add .
   git commit -m "Initial commit: MEP Data Collector v2.0 for 10th EP"
   git push origin main
   ```

### Option 2: Using Provided Files

If you have all files downloaded:

1. **Create repository** on GitHub
2. **Clone it**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/mep-data-collector.git
   ```

3. **Copy all files** maintaining the directory structure
4. **Verify structure**:
   ```bash
   cd mep-data-collector
   tree  # On Linux/Mac
   # or
   dir /s  # On Windows
   ```

5. **Commit**:
   ```bash
   git add .
   git commit -m "Initial commit: MEP Data Collector v2.0"
   git push origin main
   ```

## Verification

After setting up, verify the structure:

```bash
# Check root files
ls -la

# Check scripts directory
ls -la scripts/

# Check data directory exists
ls -la data/

# Check GitHub Actions
ls -la .github/workflows/

# Validate setup
python setup_check.py
```

Expected output from `setup_check.py`:
```
============================================================
MEP Data Collector - Setup Validation
============================================================

Checking Python version...
✓ Python version: 3.11.x

Checking dependencies...
✓ requests          - HTTP library
✓ pandas            - Data manipulation
✓ numpy             - Numerical operations
✓ bs4               - BeautifulSoup web scraping
✓ json              - JSON parsing (built-in)

Checking directory structure...
✓ Scripts directory exists
✓ All required scripts present
✓ Data directory exists

Checking optional files...
ℹ️  OpenCage API key not found (geocoding disabled)
ℹ️  GeoNames database not found (online geocoding only)
ℹ️  Disability data not found (optional)

============================================================
✓ Setup validation PASSED
============================================================
```

## Important Notes

### Files NOT in Repository

These files are generated during runtime and excluded via `.gitignore`:

- `data/*.csv` (all generated CSV files)
- `opencagekey.txt` (your actual API key)
- `venv/` or `.venv/` (virtual environments)
- `__pycache__/` (Python cache)

### Required Manual Creation

Only these need to be created manually:

- `opencagekey.txt` (if using geocoding) - copy from `.example` file
- `data/geonames.csv` (optional)
- `data/disability.csv` (optional)

## Common Setup Errors

### Error: "Directory not found"
**Cause**: Missing directory creation
**Fix**: Create missing directories with `mkdir`

### Error: "File in wrong location"
**Cause**: File placed in incorrect directory
**Fix**: Move file to correct location per tree above

### Error: ".gitkeep not showing"
**Cause**: Hidden files not visible
**Fix**: Use `ls -la` (Linux/Mac) or `dir /a` (Windows)

### Error: "GitHub Actions not running"
**Cause**: Workflow file in wrong location
**Fix**: Must be in `.github/workflows/ci.yml` exactly

## Next Steps

After verifying structure:

1. ✅ Run `python setup_check.py`
2. ✅ Review [INSTALL.md](INSTALL.md) for dependency installation
3. ✅ Read [README.md](README.md) for usage instructions
4. ✅ Run `python script.py` to collect data

## Questions?

- Check [README.md](README.md) for general usage
- See [INSTALL.md](INSTALL.md) for installation help
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Open an issue on GitHub for specific problems

---

**Current Version**: 2.0.0 (Updated for 10th European Parliament)
