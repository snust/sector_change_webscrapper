# 📈 Sector Data Scraper

A Python tool that fetches and analyzes sector performance data from StockCharts.com, providing real-time sector analysis and performance metrics.

## 🚀 Features

- Fetches real-time sector data from StockCharts API
- Supports multiple timeframe views (Intraday, Daily, Weekly, Monthly)
- Processes and structures data into a pandas DataFrame
- Extracts key metrics including:
  - Symbol and Name
  - Last Close Price
  - Price Change and Percentage Change
  - Trading Volume
  - Market Capitalization
  - SCTR (StockCharts Technical Rank)
- Automatic CSV export with timestamp

## 🛠️ Prerequisites

- Python 3.6+
- Required packages:
  ```bash
  beautifulsoup4
  requests
  pandas
  ```