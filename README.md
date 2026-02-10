# MEP Data Collector

A Python-based data collection pipeline that aggregates information about Members of the European Parliament (MEPs) from multiple sources including the European Parliament API, Wikidata, and official MEP profile pages.

## Overview

This tool collects and consolidates biographical and political data about current MEPs, including:
- Basic information (name, country, political group)
- Biographical data (birth date, birthplace, education)
- Professional background (occupations, degrees)
- Family relations
- Committee memberships
- Geographic data (birthplace coordinates)

## Data Sources

1. **European Parliament API** - Official current MEP list and metadata
2. **European Parliament Database** - Gender and additional details via RDF endpoints
3. **MEP Profile Pages** - Scraped biographical information from europarl.europa.eu
4. **Wikidata** - Enriched biographical data via SPARQL queries
5. **GeoNames** - Geographic coordinate data for birthplaces
6. **OpenCage Geocoding API** - Reverse geocoding for location classification

## Prerequisites

- Python 3.11 or higher
- pip or pipenv for package management
- OpenCage API key (for geocoding features)

## Installation

### Using pipenv (recommended)

```bash
# Clone the repository
git clone <repository-url>
cd mep-data-collector

# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell
```

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd mep-data-collector

# Install dependencies
pip install -r requirements.txt
```

## Configuration

### OpenCage API Key (Optional)

For geocoding features, create a file named `opencagekey.txt` in the project root:

```bash
echo "YOUR_API_KEY_HERE" > opencagekey.txt
```

You can obtain a free API key from [OpenCage Data](https://opencagedata.com/).

### GeoNames Data (Optional)

For offline geocoding, download the GeoNames database:

1. Download from [GeoNames](http://download.geonames.org/export/dump/)
2. Place the CSV file as `data/geonames.csv`

### Disability Data (Optional)

If you have additional disability data, place it as `data/disability.csv` with at least an `identifier` column.

## Usage

### Full Pipeline

Run the complete data collection pipeline:

```bash
python script.py
```

This will execute all steps sequentially:
1. Download initial MEP list from EP API
2. Query Parliament database for gender information
3. Scrape MEP profile pages
4. Query Wikidata for biographical data
5. Merge all data sources
6. (Optional) Geocode birthplaces

### Individual Steps

You can run individual scripts:

```bash
# Download initial list
python scripts/start.py

# Query Parliament database
python scripts/querying.py

# Scrape profiles
python scripts/scraper.py

# Query Wikidata
python scripts/getwiki.py

# Merge all data
python scripts/merger.py

# Geocode locations (optional)
python scripts/geocoding.py
```

## Output

The pipeline generates CSV files in the `data/` directory:

- `start.csv` - Initial MEP list from EP API
- `details.csv` - Gender information from Parliament database
- `scraped.csv` - Scraped biographical data
- `wikidata.csv` - Enriched data from Wikidata
- `merged.csv` - Intermediate merged dataset
- `output.csv` - Final consolidated dataset

### Output Fields

The final `output.csv` includes:
- `identifier` - Unique MEP identifier
- `name` - Full name
- `country` - Country of representation
- `group` - Political group
- `gender` - Gender
- `born_day`, `born_month`, `born_year` - Birth date components
- `born_place` - Birthplace name
- `born_lat`, `born_lon` - Birthplace coordinates
- `born_region` - Classification (native/eu/other)
- `relatives` - Family members in politics
- `highest_degree` - Highest educational degree
- `educated_at` - Educational institutions
- `occupation` - Professional background
- `memberships` - EP committee memberships

## Data Sources & Versions

This tool is currently configured for:
- **10th European Parliament** (2024-2029)
- Wikidata entity: `Q75984568`

To use for a different parliamentary term, update the Wikidata query in `scripts/getwiki.py`:

```python
FILTER(?term = wd:Q75984568).  # Change this entity ID
```

### Previous Parliamentary Terms

- 9th EP (2019-2024): `wd:Q64038205`
- 8th EP (2014-2019): `wd:Q18171345`

## Project Structure

```
mep-data-collector/
├── script.py                 # Main orchestration script
├── Pipfile                   # Pipenv dependencies
├── Pipfile.lock             # Locked dependencies
├── requirements.txt         # Pip dependencies
├── README.md                # This file
├── .gitignore              # Git ignore rules
├── opencagekey.txt         # API key (not in repo)
├── scripts/
│   ├── start.py            # Fetch initial MEP list
│   ├── querying.py         # Query Parliament database
│   ├── scraper.py          # Scrape MEP profiles
│   ├── getwiki.py          # Query Wikidata
│   ├── merger.py           # Merge all datasets
│   └── geocoding.py        # Geocode birthplaces
└── data/
    ├── start.csv           # Generated data files
    ├── details.csv
    ├── scraped.csv
    ├── wikidata.csv
    ├── merged.csv
    ├── output.csv
    ├── geonames.csv        # Optional: GeoNames database
    └── disability.csv      # Optional: Additional data
```

## Rate Limiting & Best Practices

- The European Parliament API and Wikidata SPARQL endpoint have rate limits
- The scraper includes delays between requests to avoid overwhelming servers
- For large-scale scraping, consider implementing additional delays
- The OpenCage API has a free tier limit of 2,500 requests/day

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Known Issues

- Some MEP names may differ between data sources (manual overrides in `getwiki.py`)
- Geocoding may fail for ambiguous place names
- Wikidata coverage varies by MEP

## License

MIT License - See LICENSE file for details

## Acknowledgments

Data sources:
- European Parliament Open Data Portal
- Wikidata
- GeoNames
- OpenCage Data

## Contact

For questions or issues, please open a GitHub issue.

## Changelog

### Version 2.0 (2026)
- Updated for 10th European Parliament (2024-2029)
- Improved geocoding with GeoNames database
- Enhanced error handling
- Updated dependencies

### Version 1.0 (2024)
- Initial release for 9th European Parliament
