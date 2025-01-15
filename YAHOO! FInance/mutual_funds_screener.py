import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import csv

base_url = "https://finance.yahoo.com/research-hub/screener/mutualfunds?start={start}&count=100"

desired_columns = [
    "Symbol", "Name", "1D Chart", "Price (Intraday)", "Change", "Change %",
    "Volume", "YTD Return", "3-Mo Return", "1-Year", "3-Year Return", "5-Year Return",
    "Net Expense Ratio", "Gross Expense Ratio", "Net Assets", "Morningstar Rating",
    "50 Day Avg", "200 Day Avg", "52 Week Range"
]

# Output CSV
output_file = "yahoo_finance_mutualfunds.csv"

# Write headers to the CSV file initially
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Source URL"] + desired_columns)

# Setup logging
logging.basicConfig(
    filename='finance_scraping_mutualfunds.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

# Console handler for debugging purposes
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--disable-web-security")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

combined_df = pd.DataFrame()
start_value = 0

while True:
    try:
        current_url = base_url.format(start=start_value)
        logging.info(f"Scraping {current_url}...")
        driver.get(current_url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table'))
        )
        time.sleep(1)

        table = driver.find_element(By.TAG_NAME, 'table')
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]

        page_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells):
                row_data = [cell.text.strip() for cell in cells]
                if len(row_data) == len(desired_columns):
                    page_data.append([current_url] + row_data)

        if page_data:
            with open(output_file, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(page_data)

            page_df = pd.DataFrame(page_data, columns=["Source URL"] + desired_columns)
            combined_df = pd.concat([combined_df, page_df], ignore_index=True)

        start_value += 100
        if len(rows) < 100:
            logging.info("No more pages to scrape.")
            break

    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        break

# Close WebDriver
driver.quit()

logging.info(f"Data successfully scraped and saved to {output_file}.")
print(f"Data successfully scraped and saved to {output_file}.")