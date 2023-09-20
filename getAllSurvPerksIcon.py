import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

url = "https://deadbydaylight.fandom.com/wiki/Perks"

chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

chromedriver_path = "/usr/bin/chromedriver"
service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')

wikitable = soup.find('table', class_='wikitable sortable jquery-tablesorter')

if wikitable:
    perks_images = wikitable.find_all('img', {'data-src': True})
    
    pattern = r'(https:\/\/.*?\.png)'
    img_dir = "img"
    
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    
    for image in perks_images:
        data_src_value = image['data-src']
        match = re.search(pattern, data_src_value)
        if match:
            extracted_url = match.group(0)
            if "IconPerks" in extracted_url:
                image_name = os.path.basename(extracted_url)
                destination_path = os.path.join(img_dir, image_name)
                response = requests.get(extracted_url)
                with open(destination_path, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"Image téléchargée : {image_name}")
else:
    print("Tableau introuvable.")

driver.quit()
