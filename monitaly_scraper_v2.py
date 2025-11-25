#!/usr/bin/env python3
"""
Monitaly Stockists Web Scraper - Improved Version
This version is specifically tailored to the Monitaly website structure.
"""

import requests
from bs4 import BeautifulSoup
import csv
import re

def scrape_monitaly_stockists(url="https://www.monitaly.com/stockists"):
    """
    Scrape Monitaly stockists page.
    The page structure has country headers followed by stockist blocks.
    Each stockist block contains: Name (link), City, Social handle (link with @)
    """
    
    print(f"Fetching {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    stockists = []
    
    # Countries list for reference
    countries = [
        'Australia', 'Belgium', 'Canada', 'France', 'Germany', 'Hong Kong',
        'Italy', 'Japan', 'Korea', 'Mexico', 'Netherlands', 'Switzerland',
        'Taiwan', 'UK', 'USA'
    ]
    
    current_country = None
    
    # Find the main content container
    main_content = soup.find('div', class_='sqs-block-content')
    if not main_content:
        # Fallback to body
        main_content = soup.body
    
    # Iterate through all paragraphs and headers
    for element in main_content.find_all(['h2', 'h3', 'p']):
        text = element.get_text(strip=True)
        
        # Check if this is a country header
        if text in countries:
            current_country = text
            print(f"\nProcessing country: {current_country}")
            continue
        
        # Skip if no country set yet
        if not current_country:
            continue
        
        # Process stockist entries
        # Look for elements with links (stockist entries typically have links)
        links = element.find_all('a')
        
        if links and len(links) >= 1:
            # Extract all text pieces in order
            text_parts = list(element.stripped_strings)
            
            if len(text_parts) >= 2:
                # First part is usually the stockist name
                stockist_name = text_parts[0]
                
                # Second part is usually the city
                city = text_parts[1]
                
                # Find the social media link (usually marked with @)
                social_link = ""
                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if link_text.startswith('@'):
                        # This is the social media handle
                        if 'instagram.com' in href:
                            social_link = href
                        else:
                            # Construct Instagram URL from handle
                            handle = link_text.replace('@', '').strip()
                            social_link = f"https://www.instagram.com/{handle}/"
                        break
                
                # Add to results if we have the minimum required info
                if stockist_name and city:
                    stockist_entry = {
                        'country': current_country,
                        'stockist': stockist_name,
                        'city': city,
                        'social_link': social_link
                    }
                    stockists.append(stockist_entry)
                    print(f"  Added: {stockist_name} - {city}")
    
    return stockists

def clean_text(text):
    """Remove extra whitespace and clean text"""
    return re.sub(r'\s+', ' ', text).strip()

def save_to_csv(stockists, filename='monitaly_stockists.csv'):
    """Save stockists data to CSV file"""
    
    if not stockists:
        print("No stockists to save!")
        return
    
    print(f"\nSaving {len(stockists)} stockists to {filename}...")
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['COUNTRY', 'STOCKIST', 'CITY', 'SOCIAL LINK']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for stockist in stockists:
            writer.writerow({
                'COUNTRY': stockist['country'],
                'STOCKIST': stockist['stockist'],
                'CITY': stockist['city'],
                'SOCIAL LINK': stockist['social_link']
            })
    
    print(f"✓ Successfully saved to {filename}")
    return filename

def print_summary(stockists):
    """Print a summary of scraped data"""
    
    if not stockists:
        print("\nNo stockists found!")
        return
    
    print("\n" + "="*80)
    print(f"SUMMARY: Found {len(stockists)} stockists")
    print("="*80)
    
    # Count by country
    country_counts = {}
    for stockist in stockists:
        country = stockist['country']
        country_counts[country] = country_counts.get(country, 0) + 1
    
    print("\nStockists by country:")
    for country, count in sorted(country_counts.items()):
        print(f"  {country}: {count}")
    
    print("\n" + "="*80)
    print("Sample entries:")
    print("="*80)
    for i, stockist in enumerate(stockists[:5], 1):
        print(f"\n{i}. {stockist['country']}")
        print(f"   Stockist: {stockist['stockist']}")
        print(f"   City: {stockist['city']}")
        print(f"   Social: {stockist['social_link']}")

def main():
    """Main execution function"""
    
    print("Monitaly Stockists Scraper")
    print("="*80)
    
    try:
        # Scrape the website
        stockists = scrape_monitaly_stockists()
        
        # Print summary
        print_summary(stockists)
        
        # Save to CSV
        if stockists:
            filename = save_to_csv(stockists)
            print(f"\n✓ Data has been saved to: {filename}")
            print("\nYou can now open this CSV file in Excel, Google Sheets, or any spreadsheet program.")
        else:
            print("\n⚠ No stockists were found. The website structure may have changed.")
            print("Please check the website manually or update the scraper.")
            
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Error fetching the website: {e}")
        print("Please check your internet connection and try again.")
    except Exception as e:
        print(f"\n✗ An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
