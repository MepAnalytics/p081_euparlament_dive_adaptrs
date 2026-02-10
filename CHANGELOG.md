# Changelog

All notable changes to the MEP Data Collector project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-10

### Changed
- **BREAKING**: Updated for 10th European Parliament (2024-2029)
- Updated Wikidata SPARQL query to use entity `wd:Q75984568` (10th EP)
- Improved error handling across all scripts
- Enhanced progress reporting with step counters
- Better logging and user feedback

### Added
- Comprehensive README.md with detailed documentation
- CONTRIBUTING.md with contribution guidelines
- requirements.txt for pip users
- .gitignore for better repository hygiene
- LICENSE file (MIT)
- Improved geocoding with GeoNames database support
- Better handling of missing data
- API rate limiting considerations

### Fixed
- Improved name matching between data sources
- Better handling of special characters in names
- Fixed date parsing edge cases
- Improved error messages

### Documentation
- Complete README with usage examples
- Installation instructions for both pipenv and pip
- Configuration guide for API keys
- Project structure documentation
- Troubleshooting section

## [1.0.0] - 2024-06-15

### Added
- Initial release for 9th European Parliament (2019-2024)
- Data collection from European Parliament API
- Parliament database querying for gender information
- Web scraping of MEP profile pages
- Wikidata integration via SPARQL queries
- Data merging pipeline
- Optional geocoding functionality
- Basic documentation

### Features
- Automated data pipeline for MEP biographical data
- Multi-source data integration
- Biographical data enrichment
- Educational background classification
- Professional occupation categorization
- Geographic birth data

---

## Version History

### [2.0.0] - February 2026
Updated for 10th European Parliament with improved error handling and documentation

### [1.0.0] - June 2024
Initial release for 9th European Parliament

---

## Migration Guide

### From 1.x to 2.0

If you're upgrading from version 1.x:

1. **Update the Wikidata query** in `scripts/getwiki.py`:
   - Old: `FILTER(?term = wd:Q64038205).`  # 9th EP
   - New: `FILTER(?term = wd:Q75984568).`  # 10th EP

2. **Review name overrides** in `scripts/getwiki.py`:
   - Some MEPs from the 9th term may no longer be serving
   - New MEPs may need name matching overrides

3. **Update your dependencies**:
   ```bash
   pipenv update
   ```
   or
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **Test the pipeline**:
   ```bash
   python script.py
   ```

## Reporting Issues

If you encounter issues with a specific version:
- Check the relevant section in this changelog
- Review closed issues on GitHub
- Open a new issue with version information

## Future Versions

### Planned for 2.1.0
- Improved error recovery
- Better handling of special characters
- Performance optimizations
- Additional data sources
- Enhanced documentation

### Under Consideration
- Support for historical parliamentary terms
- Database backend option
- API for data access
- Automated data updates
- Visualization tools

---

For detailed information about each change, see the Git commit history or release notes.
