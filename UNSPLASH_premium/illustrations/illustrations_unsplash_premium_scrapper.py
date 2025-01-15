import os
import re
import time
import logging
import requests
from tqdm import tqdm
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#logging
logging.basicConfig(
    filename='UNSPLASH_premium/illustrations/LOGS/image_downloader.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

# Get keywords from the user
keywords = input("Enter keywords separated by commas: ").split(',')

# Create the saves directory
saves_dir = 'UNSPLASH_premium//illustrations/SAVES'
os.makedirs(saves_dir, exist_ok=True)
logging.info(f"Created directory: {saves_dir}")

def sanitize_filename(filename):
    sanitized_filename = re.sub(r'[\\/*?:"<>|]', "_", filename)
    return sanitized_filename

def download_image(url, folder, retries=3):
    while retries > 0:
        try:
            logging.info(f"Downloading image from {url}")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                filename = sanitize_filename(os.path.basename(url)) + '.jpg'
                img_path = os.path.join(folder, filename)
                img.save(img_path)
                logging.info(f"Image saved: {img_path}")
                return True
            else:
                logging.error(f"Failed to download {url} - Status code: {response.status_code}")
            retries -= 1
            time.sleep(2)
        except Exception as e:
            logging.error(f"Failed to download {url} - {e}")
            retries -= 1
            time.sleep(2)
    return False

def scroll_and_load_images(driver, keyword_dir):
    downloaded_images = set()
    logging.info("Starting infinite scroll.")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        images = soup.find_all('img', {'src': True})

        new_images_found = 0
        for img in images:
            img_url = img['src']
            if img_url and img_url.startswith('http') and img_url not in downloaded_images:
                if download_image(img_url, keyword_dir):
                    downloaded_images.add(img_url)
                    new_images_found += 1
        
        if new_images_found > 0:
            logging.info(f"{new_images_found} new images downloaded for '{keyword_dir}': Total {len(downloaded_images)} images downloaded.")
        else:
            logging.info("No new images found this scroll.")

            print("Please manually click the 'Load more' button to load additional images.")

            while True:
                user_input = input("Type 'done' when you have finished loading images or 'continue' to proceed: ")
                if user_input.strip().lower() == 'done':
                    break
                elif user_input.strip().lower() == 'continue':
                    continue
                else:
                    print("Please type 'done' or 'continue'.")

def search_images(keyword, saves_dir):
    keyword_dir = os.path.join(saves_dir, keyword.strip())
    os.makedirs(keyword_dir, exist_ok=True)
    logging.info(f"Created directory for keyword '{keyword}': {keyword_dir}")

    search_url = f"https://unsplash.com/{keyword.strip()}/illustrations"
    logging.info(f"Searching images for keyword '{keyword}' at {search_url}")

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(search_url)

    scroll_and_load_images(driver, keyword_dir)

    driver.quit()

for keyword in keywords:
    search_images(keyword, saves_dir)

logging.info('Image downloading complete.')
print("Image downloading complete.")