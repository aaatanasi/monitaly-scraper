# Monitaly Stockists Web Scraper

This Python script scrapes stockist information from https://www.monitaly.com/stockists and exports it to a CSV file.

## What it extracts

The scraper extracts the following information for each stockist:
- **COUNTRY**: The country where the stockist is located (e.g., "Australia", "Belgium", "USA")
- **STOCKIST**: The name of the store/stockist (e.g., "PPHH", "Yatahey")
- **CITY**: The city or location (e.g., "Fitzroy", "Tournai")
- **SOCIAL LINK**: The social media link, typically Instagram (e.g., "https://www.instagram.com/pphstore/")

## Installation

1. Make sure you have Python 3.7 or higher installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install requests beautifulsoup4 lxml
```

## Usage

Simply run the script:

```bash
python monitaly_scraper_v2.py
```

The script will:
1. Fetch the stockists page from Monitaly
2. Parse the HTML and extract all stockist information
3. Save the data to `monitaly_stockists.csv`
4. Print a summary of the scraped data

## Output

The script creates a CSV file named `monitaly_stockists.csv` with the following format:

```
COUNTRY,STOCKIST,CITY,SOCIAL LINK
Australia,PPHH,Fitzroy,https://www.instagram.com/pphstore/
Belgium,Yatahey,Tournai,https://www.instagram.com/yatahey_tournai/
...
```

You can open this file in:
- Microsoft Excel
- Google Sheets
- Any spreadsheet application
- Text editors

## Example Output

```
Australia, PPHH, Fitzroy, https://www.instagram.com/pphstore/
Belgium, Yatahey, Tournai, https://www.instagram.com/yatahey_tournai/
Canada, Centre Commercial, Paris, https://www.instagram.com/centre_commercial/
```

## Troubleshooting

**"No stockists found"**
- The website structure may have changed
- Check your internet connection
- Try running the script again

**"Module not found" error**
- Make sure you've installed all dependencies: `pip install -r requirements.txt`

**"Connection error"**
- Check your internet connection
- The website might be temporarily down
- Try again later

## Files Included

- `monitaly_scraper_v2.py` - Main scraper script (recommended)
- `monitaly_scraper.py` - Alternative version with different parsing approach
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Notes

- The scraper respects the website's content and only extracts publicly available information
- Run time is typically 2-5 seconds depending on your internet connection
- The script handles Instagram links and @ handles automatically

## License

This script is provided as-is for personal use.
