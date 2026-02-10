# Contributing to MEP Data Collector

Thank you for your interest in contributing to the MEP Data Collector project! This document provides guidelines for contributions.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your Python version and OS
- Relevant error messages or logs

### Suggesting Enhancements

We welcome suggestions for new features or improvements:
- Open an issue describing your idea
- Explain the use case and benefits
- If possible, sketch out how it might work

### Pull Requests

1. **Fork the repository** and create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, documented code
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

3. **Test your changes**
   - Run the full pipeline to ensure nothing breaks
   - Test edge cases
   - Verify output data quality

4. **Commit your changes**
   - Write clear commit messages
   - Reference issue numbers if applicable
   ```bash
   git commit -m "Add feature: description (#issue-number)"
   ```

5. **Push to your fork** and create a pull request
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Describe your PR**
   - Explain what changes you made and why
   - Reference any related issues
   - Note any breaking changes

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/mep-data-collector.git
cd mep-data-collector

# Install dependencies
pipenv install --dev

# Activate virtual environment
pipenv shell
```

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Keep functions focused and single-purpose
- Maximum line length: 100 characters
- Use docstrings for functions and modules

### Documentation
- Update README.md for user-facing changes
- Comment complex algorithms
- Keep documentation up to date

### Data Processing
- Handle missing data gracefully
- Use pandas best practices
- Include error handling and logging
- Validate data at each step

## Project Structure

```
mep-data-collector/
├── script.py              # Main pipeline orchestrator
├── scripts/               # Individual processing scripts
│   ├── start.py          # Step 1: Fetch MEP list
│   ├── querying.py       # Step 2: Query Parliament DB
│   ├── scraper.py        # Step 3: Scrape profiles
│   ├── getwiki.py        # Step 4: Query Wikidata
│   ├── merger.py         # Step 5: Merge data
│   └── geocoding.py      # Step 6: Geocode (optional)
└── data/                 # Output directory

```

## Testing

Before submitting a PR:

1. **Run the full pipeline**
   ```bash
   python script.py
   ```

2. **Check output quality**
   - Verify `data/output.csv` exists
   - Check for expected number of MEPs
   - Spot-check a few records for accuracy

3. **Test individual scripts** if you modified specific steps
   ```bash
   python scripts/start.py
   python scripts/querying.py
   # etc.
   ```

## Common Tasks

### Updating for a New Parliamentary Term

When a new European Parliament term begins:

1. Find the Wikidata entity ID for the new term
2. Update `scripts/getwiki.py`:
   ```python
   FILTER(?term = wd:QXXXXXXXX).  # New term entity
   ```
3. Update version number in README.md
4. Test with the new data

### Adding New Data Sources

To integrate a new data source:

1. Create a new script in `scripts/`
2. Add it to the pipeline in `script.py`
3. Update merger logic in `scripts/merger.py`
4. Document in README.md

### Improving Data Quality

To enhance data accuracy:

1. Review categorization dictionaries in scripts
2. Add missing keywords or categories
3. Improve name matching logic
4. Handle edge cases better

## Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Check existing issues and discussions
- Review the README.md for basic usage

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Other unethical or unprofessional conduct

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Attribution

Contributors will be recognized in the project. Significant contributions may be highlighted in release notes.

Thank you for contributing to MEP Data Collector! 🇪🇺
