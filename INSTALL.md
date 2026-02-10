# Installation Guide - MEP Data Collector

Complete step-by-step installation instructions for the MEP Data Collector project.

## Table of Contents
- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Post-Installation Setup](#post-installation-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.11 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB for dependencies and data
- **Internet**: Required for API access and data collection

### Check Your Python Version
```bash
python --version
# or
python3 --version
```

If you don't have Python 3.11+, download from [python.org](https://www.python.org/downloads/)

## Installation Methods

### Method 1: Using Pipenv (Recommended)

Pipenv provides isolated environments and dependency management.

#### Step 1: Install Pipenv
```bash
pip install pipenv
```

#### Step 2: Clone Repository
```bash
git clone https://github.com/YOUR-USERNAME/mep-data-collector.git
cd mep-data-collector
```

#### Step 3: Install Dependencies
```bash
pipenv install
```

#### Step 4: Activate Virtual Environment
```bash
pipenv shell
```

You should now see `(mep-data-collector)` in your terminal prompt.

### Method 2: Using pip with venv

Standard Python virtual environment approach.

#### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR-USERNAME/mep-data-collector.git
cd mep-data-collector
```

#### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

#### Step 3: Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Method 3: Global Installation (Not Recommended)

Install dependencies globally without virtual environment.

```bash
git clone https://github.com/YOUR-USERNAME/mep-data-collector.git
cd mep-data-collector
pip install -r requirements.txt
```

**Warning**: This may conflict with other Python projects.

## Post-Installation Setup

### 1. Verify Installation

Run the setup check script:
```bash
python setup_check.py
```

This will verify:
- ✓ Python version
- ✓ All required dependencies
- ✓ Directory structure
- ℹ️ Optional files status

### 2. Optional: Configure Geocoding

If you want to enable geocoding features:

#### Get OpenCage API Key
1. Visit [https://opencagedata.com/](https://opencagedata.com/)
2. Sign up for free account (2,500 requests/day)
3. Copy your API key

#### Create API Key File
```bash
# Copy the example file
cp opencagekey.txt.example opencagekey.txt

# Edit the file and replace with your actual key
# On Linux/Mac:
echo "YOUR_ACTUAL_API_KEY_HERE" > opencagekey.txt

# On Windows, use a text editor to edit opencagekey.txt
```

### 3. Optional: Download GeoNames Database

For offline geocoding (optional):

1. Visit [GeoNames Download](http://download.geonames.org/export/dump/)
2. Download `allCountries.zip` or a specific country file
3. Extract and prepare the CSV
4. Place as `data/geonames.csv`

**Required columns**: Name, Alternate Names, Coordinates, Population

### 4. Optional: Add Custom Data

If you have additional MEP data:

#### Disability Data
Create `data/disability.csv` with at least:
```csv
identifier;disability_info
123456;value
```

## Verification

### Quick Test Run

Test individual scripts:

```bash
# Test Step 1: Fetch MEP list
python scripts/start.py

# Check output
ls -l data/start.csv  # Linux/Mac
dir data\start.csv    # Windows
```

If `data/start.csv` is created with ~720 MEPs, installation is successful!

### Full Pipeline Test

Run the complete pipeline:
```bash
python script.py
```

Expected output:
```
============================================================
MEP DATA COLLECTION PIPELINE
European Parliament - 10th Term (2024-2029)
============================================================

Step 1/5: Downloading initial MEP list from EP API
✓ Successfully downloaded 720 MEPs
...
```

## Troubleshooting

### Common Issues

#### Issue: "Python not found"
**Solution**: Install Python 3.11+ from [python.org](https://www.python.org/downloads/)

#### Issue: "pip not found"
**Solution**: 
```bash
python -m ensurepip --upgrade
```

#### Issue: "Permission denied" when installing
**Solution**: 
- Use virtual environment (recommended)
- Or use `pip install --user -r requirements.txt`
- On Linux/Mac: Don't use `sudo pip`

#### Issue: "Module not found" errors
**Solution**:
```bash
# Verify you're in virtual environment
# Then reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### Issue: API requests failing
**Solutions**:
- Check internet connection
- Verify firewall isn't blocking requests
- Check if European Parliament APIs are accessible from your location
- Try using a VPN if blocked

#### Issue: Slow performance
**Solutions**:
- Normal for first run (scraping 720+ profiles)
- Ensure good internet connection
- Don't reduce delays in scraper.py (respects server limits)

#### Issue: Character encoding errors
**Solution**:
```bash
# Set UTF-8 encoding
# Windows:
set PYTHONIOENCODING=utf-8

# Linux/Mac:
export PYTHONIOENCODING=utf-8
```

### Platform-Specific Issues

#### Windows

**Issue**: `'python' is not recognized`
**Solution**: Use `python` or `py` command, ensure Python is in PATH

**Issue**: Script execution policy errors
**Solution**: 
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS

**Issue**: SSL certificate errors
**Solution**:
```bash
/Applications/Python\ 3.11/Install\ Certificates.command
```

#### Linux

**Issue**: Missing system dependencies
**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3-pip

# Fedora/RHEL
sudo dnf install python3.11 python3-pip
```

### Getting Help

If you encounter issues:

1. **Check existing issues**: [GitHub Issues](https://github.com/YOUR-USERNAME/mep-data-collector/issues)
2. **Run diagnostics**: `python setup_check.py`
3. **Create new issue**: Include error message and system info

## Next Steps

After successful installation:

1. Read the [README.md](README.md) for usage instructions
2. Review [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
3. Run `python script.py` to collect MEP data
4. Explore the output in `data/output.csv`

## Updating

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pipenv update  # if using pipenv
# or
pip install --upgrade -r requirements.txt  # if using pip
```

## Uninstalling

To remove the project:

```bash
# Exit virtual environment (if active)
deactivate  # or exit pipenv shell

# Remove project directory
cd ..
rm -rf mep-data-collector  # Linux/Mac
# or
rmdir /s mep-data-collector  # Windows
```

---

**Need help?** Open an issue on GitHub or check the troubleshooting section above.
