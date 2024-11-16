from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import time

def get_sector_data(group="SECTOR_SPDR", view="E"):
    """
    Fetch sector data from StockCharts API
    
    Args:

        group (str): Sector group (default: SECTOR_SPDR)
        view (str): Data view type:
            - 'I': Intraday
            - 'E': End of day
            - 'W': Weekly
            - 'M': Monthly
            etc.
    
    Returns:
        pandas.DataFrame: Processed sector data
    """
    
    # API endpoint
    url = "https://stockcharts.com/j-sum/sum"
    
    # Request parameters
    params = {
        "cmd": "perf",
        "group": group,
        "view": view,
        "r": int(time.time() * 1000)  # Current timestamp in milliseconds
    }
    
    # Headers to mimic browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://stockcharts.com/freecharts/sectorsummary.html",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    try:
        # Make the request
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Get JSON data
        data = response.json()
        
        # Process the data into a list of dictionaries
        processed_data = []
        for item in data:
            if isinstance(item, dict) and 'sym' in item:  # Only process items with symbol data
                processed_item = {
                    'Symbol': item.get('sym', ''),
                    'Name': item.get('name', ''),
                    'Last Close': item.get('lastClose', ''),
                    'Change': item.get('chg', '').split(',')[0] if item.get('chg') else '',
                    'Pct Change': item.get('pctChg', '').split(',')[0] if item.get('pctChg') else '',
                    'Volume': item.get('volume', ''),
                    'Market Cap': item.get('marketCap', ''),
                    'SCTR': item.get('sctr', '')
                }
                processed_data.append(processed_item)
        
        # Convert to DataFrame
        df = pd.DataFrame(processed_data)
        
        # Convert numeric columns
        numeric_columns = ['Last Close', 'Change', 'Pct Change', 'Volume', 'Market Cap', 'SCTR']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col])
        
        return df
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_csv(df, filename=None):
    """
    Save the DataFrame to a CSV file
    """
    if filename is None:
        filename = f"sector_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    # Fetch the data
    df = get_sector_data()
    
    if df is not None:
        # Display first few rows
        print("\nFirst few rows of the data:")
        print(df.head())
        
        # Display basic statistics
        print("\nBasic statistics:")
        print(df.describe())
        
        # Save to CSV
        save_to_csv(df)
    
if __name__ == "__main__":
    main()