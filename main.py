from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import re
import json
import os
import pandas as pd

# Open the CSV file in append mode
with open('vets_in_LA.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    # Write the headers only if the file is empty
    if file.tell() == 0:
        writer.writerow(["Company Name", "Phone Number", "Address", "Company URL"])

if os.path.exists('vets_in_LA.csv'):
    # If the file exists, load the data
    df = pd.read_csv('vets_in_LA.csv')
    visited_urls = set(df["Company URL"].tolist())
else:
    # If the file doesn't exist, initialize an empty set
    visited_urls = set()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors=yes')
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

def get_company_info(driver, writer):
    # Get the company's name
    company_name_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "y-css-olzveb"))
    )
    company_name = company_name_element.text

    # Get the phone number
    phone_number = "Number not found" 
    try:
        phone_number_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'y-css-1lfp6nf')]//p[contains(@class, 'y-css-1o34y7f') and contains(text(), '(')]"))
        )
        phone_number_text = phone_number_element.text
        # Looks for the (xxx) xxx-xxxx
        phone_number_match = re.search(r'\(\d{3}\) \d{3}-\d{4}', phone_number_text)
        # Returns exactly (xxx) xxx-xxxx
        phone_number = phone_number_match.group(0)
    except:
        print("Company number not found")

    # Get the address
    address = "Address not found"
    try:
        address_elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "y-css-dg8xxd"))
        )
        # There are different texts with the same class for address, so search for the ones that start with at least 3 digits
        for element in address_elements:
            if re.search(r'\d{3,}.*', element.text):
                address = element.text
                break
    except:
        print("Address not found")

    # Write data to CSV
    writer.writerow([company_name, phone_number, address, company_url])
    print(f"Company name, number, and address written to vets_in_LA.csv: {company_name}, {phone_number}, {address} {company_url}")

try:
    driver.get("https://www.yelp.com")

    search_field = driver.find_element(By.ID, "search_description")
    location_field = driver.find_element(By.ID, "search_location")

    search_field.clear()
    search_field.send_keys("vets")
    location_field.send_keys(Keys.CONTROL + "a")
    location_field.send_keys(Keys.DELETE)
    location_field.send_keys("Los Angeles, CA")
    location_field.send_keys(Keys.RETURN)
    page_number = 1

    while True:
        error_count = 0
        # Grabs every result that isnt sponsored (1-10 each page)
        for i in range(13, 24):
            try:
                # Find the company link
                company_link = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f'//*[@id="main-content"]/ul/li[{i}]/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h3/a[not(contains(@href, "/url_redacted"))]'))
                )
                company_url = company_link.get_attribute('href')

                if company_url in visited_urls:
                    print("Already seen")
                    continue

                visited_urls.add(company_url)
                driver.get(company_url)

                with open('vets_in_LA.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    get_company_info(driver, writer)

                # Go back to the search results
                driver.execute_script("window.history.go(-1)")

            except:
                print(f"Error processing result at index {i}")
                # if 2+ error, go to next page
                error_count += 1
                if error_count > 2:
                    break

        # Click on the next page
        try:
            next_page_link = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "icon--24-chevron-right-v2"))
            )
            next_page_link.click()
            page_number += 1
        except:
            print("No more pages or error navigating to the next page.")
            break

finally:
    driver.quit()