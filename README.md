# Web Scraping Scripts

## Description

Welcome to the **Web Scraping Scripts** project! This repository contains various scripts designed to extract data from different sources such as Google Trends, Unsplash, and Yahoo Finance. These scripts utilize powerful libraries including Selenium, Chrome WebDriver, Requests, BeautifulSoup4, lxml, csv, and Pillow to perform the scraping tasks and save the extracted data into CSV files.

## Developer Contact

For any queries or issues, please contact the [developer](mailto:a91060705@gmail.com)

## Project Structure

- **.venv/**: Virtual environment directory.
- **google_trends/**: Contains scripts and data related to Google Trends scraping.
  - `google_trends_europe.csv`: CSV file containing Google Trends data for Europe.
  - `trends.py`: Python script for scraping Google Trends data.
- **UNSPLASH_premium/illustrations/**: Contains scripts and data related to Unsplash premium illustrations scraping.
  - `illustrations_unsplash_premium_scrapper.py`: Python script for scraping Unsplash premium illustrations.
  - **LOGS/**: Directory for log files.
  - **SAVES/**: Directory for saved data.
- **YAHOO! Finance/**: Contains scripts and data related to Yahoo Finance scraping.
  - `mutual_funds_screener.py`: Python script for scraping Yahoo Finance mutual funds data.
  - `finance_scraping_mutualfunds.log`: Log file for Yahoo Finance scraping.
  - `yahoo_finance_mutualfunds.csv`: CSV file containing Yahoo Finance mutual funds data.
- `README.md`: Project documentation file.
- `requirements.txt`: List of project dependencies.

## Requirements

- Python 3.x
- Selenium
- Chrome WebDriver
- Requests
- BeautifulSoup4
- lxml
- csv
- Pillow

## Setup Instructions

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure the virtual environment is activated.
2. Run the desired script using Python:
   ```bash
   python path/to/script.py
