# MEP Data Collector - Complete Repository Structure

## 📁 Project Overview

This repository contains a complete data collection pipeline for Members of the European Parliament (MEPs). Updated for the 10th European Parliament (2024-2029).

## 📂 Directory Structure

```
mep-data-collector/
│
├── 📄 README.md                    # Main documentation
├── 📄 LICENSE                      # MIT License
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 CHANGELOG.md                 # Version history
├── 📄 Pipfile                      # Pipenv dependencies
├── 📄 Pipfile.lock                 # Locked dependencies
├── 📄 requirements.txt             # Pip dependencies
├── 📄 .gitignore                   # Git ignore rules
├── 📄 setup_check.py               # Environment validation script
├── 📄 script.py                    # Main pipeline orchestrator
├── 📄 opencagekey.txt.example      # API key template
│
├── 📁 scripts/                     # Data collection scripts
│   ├── 📄 __init__.py             # Package init
│   ├── 📄 start.py                # Step 1: Fetch MEP list from EP API
│   ├── 📄 querying.py             # Step 2: Query Parliament database
│   ├── 📄 scraper.py              # Step 3: Scrape MEP profiles
│   ├── 📄 getwiki.py              # Step 4: Query Wikidata (UPDATED for 10th EP)
│   ├── 📄 merger.py               # Step 5: Merge all datasets
│   └── 📄 geocoding.py            # Step 6: Geocode birthplaces (optional)
│
├── 📁 data/                        # Data directory (generated files)
│   ├── 📄 .gitkeep                # Preserves directory in git
│   ├── 📄 start.csv               # Generated: Initial MEP list
│   ├── 📄 details.csv             # Generated: Gender information
│   ├── 📄 scraped.csv             # Generated: Scraped biographical data
│   ├── 📄 wikidata.csv            # Generated: Wikidata enrichment
│   ├── 📄 merged.csv              # Generated: Intermediate merge
│   ├── 📄 output.csv              # Generated: Final consolidated dataset
│   ├── 📄 geonames.csv            # Optional: GeoNames database
│   └── 📄 disability.csv          # Optional: Additional data
│
└── 📁 .github/                     # GitHub configuration
    └── 📁 workflows/
        └── 📄 ci.yml              # GitHub Actions CI/CD

```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd mep-data-collector
```

### 2. Install Dependencies
**Using pipenv (recommended):**
```bash
pipenv install
pipenv shell
```

**Using pip:**
```bash
pip install -r requirements.txt
```

### 3. Validate Setup
```bash
python setup_check.py
```

### 4. Run Pipeline
```bash
python script.py
```

## 📊 Data Flow

```
┌─────────────────┐
│  EP API         │  Step 1: start.py
│  (Initial List) │ ──────────┐
└─────────────────┘           │
                               ▼
┌─────────────────┐      ┌──────────┐
│  Parliament DB  │      │ start.csv│
│  (Gender Info)  │ ───► │          │
└─────────────────┘      └──────────┘
                               │
┌─────────────────┐           │
│  MEP Profiles   │  Step 2-3 │
│  (Scraping)     │ ──────────┤
└─────────────────┘           │
                               ▼
┌─────────────────┐      ┌──────────────┐
│  Wikidata       │      │ Multiple CSVs│
│  (Biographical) │ ───► │              │
└─────────────────┘      └──────────────┘
                               │
                         Step 5: Merger
                               │
                               ▼
                         ┌──────────┐
                         │output.csv│ ◄─── Final Dataset
                         └──────────┘
                               │
                  Optional Step 6: Geocoding
                               │
                               ▼
                         ┌──────────┐
                         │output.csv│ ◄─── With coordinates
                         └──────────┘
```

## 🔧 Configuration

### Required
None! The pipeline works out of the box.

### Optional
- **opencagekey.txt**: For geocoding features
  - Get free API key: https://opencagedata.com/
  - Save to project root

- **data/geonames.csv**: For offline geocoding
  - Download from: http://download.geonames.org/export/dump/

- **data/disability.csv**: For additional MEP data
  - Custom dataset with `identifier` column

## 📝 Key Features

### Updated for 10th European Parliament
- ✅ Wikidata query updated to `wd:Q75984568`
- ✅ Compatible with current MEP data (2024-2029)

### Improved Pipeline
- ✅ Better error handling and logging
- ✅ Progress indicators for long-running tasks
- ✅ Graceful handling of missing data
- ✅ Rate limiting for API calls

### Comprehensive Documentation
- ✅ Detailed README with examples
- ✅ Contribution guidelines
- ✅ Changelog for version tracking
- ✅ Setup validation script

### Developer Friendly
- ✅ Clean code structure
- ✅ Docstrings and comments
- ✅ GitHub Actions CI/CD ready
- ✅ Both pipenv and pip support

## 📊 Output Fields

The final `output.csv` includes:

| Field | Description |
|-------|-------------|
| identifier | Unique MEP identifier |
| name | Full name |
| givenName | First name |
| familyName | Last name |
| country | Country of representation |
| group | Political group |
| gender | Gender |
| born_day | Birth day |
| born_month | Birth month |
| born_year | Birth year |
| born_place | Birthplace name |
| born_lat | Birthplace latitude (if geocoded) |
| born_lon | Birthplace longitude (if geocoded) |
| born_region | Region classification (native/eu/other) |
| relatives | Family members in politics |
| highest_degree | Highest educational degree |
| educated_at | Educational institutions |
| occupation | Professional background |
| memberships | EP committee memberships |

## 🔄 Updating for Future Parliamentary Terms

When a new EP term begins:

1. Find the Wikidata entity ID for the new term
2. Update in `scripts/getwiki.py`:
   ```python
   FILTER(?term = wd:QXXXXXXXX).
   ```
3. Update version in README.md and CHANGELOG.md
4. Test the pipeline

### Previous Terms
- 10th EP (2024-2029): `wd:Q75984568` ← **Current**
- 9th EP (2019-2024): `wd:Q64038205`
- 8th EP (2014-2019): `wd:Q18171345`

## 🐛 Troubleshooting

### Setup Issues
Run `python setup_check.py` to diagnose

### API Errors
- Check internet connection
- Verify rate limits haven't been exceeded
- Check if APIs are accessible from your location

### Data Quality
- Review manual name overrides in `getwiki.py`
- Check categorization dictionaries in scripts
- Verify source data hasn't changed format

## 📚 Additional Resources

- European Parliament API: https://data.europarl.europa.eu/
- Wikidata SPARQL: https://query.wikidata.org/
- GeoNames: http://www.geonames.org/
- OpenCage Geocoding: https://opencagedata.com/

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - See [LICENSE](LICENSE) file.

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Version 2.0.0** - Updated for 10th European Parliament (2024-2029)
