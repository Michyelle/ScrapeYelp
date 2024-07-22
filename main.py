from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import openpyxl
import time

try:
    chrome_options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.yelp.com")

    search_field = driver.find_element(By.ID, "search_description")
    location_field = driver.find_element(By.ID, "search_location")
    print("located boxes")
    time.sleep(5)

    search_field.clear()
    search_field.send_keys("veterinaries")
    location_field.send_keys(Keys.CONTROL + "a")
    location_field.send_keys(Keys.DELETE)
    location_field.send_keys("Los Angeles, CA")
    print("inputted keywords")
    time.sleep(5)


    location_field.send_keys(Keys.RETURN)
    print("entered values")
    time.sleep(10)


except:
    print("did not work")

"""    1. click on the first company on the list
        - write the company's name down on excel
        - write the company's number down on excel
    2. click back, click on the next company on the list
        - repeat
    if end of the list, click on the next page and repeat the process"""




def update_form_field(driver, field_name, field_value):
    search_bar = driver.find_element(By.ID, field_name)
    search_bar.clear()
    time.sleep(1)
    search_bar.send_keys(field_value)

def extract_and_write_data(driver, sheet):
    company_name = driver.find_element(By.CSS_SELECTOR, "h1.css-11q1g5y").text
    phone_number = driver.find_element(By.CSS_SELECTOR, "p.css-8jxw1i").text
    sheet.append([company_name, phone_number])

# Initialize the Chrome driver
chrome_options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Create a new Excel workbook and sheet
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Veterinaries in LA"
sheet.append(["Company Name", "Phone Number"])

try:
    driver.get("https://www.yelp.com")

    search_field = driver.find_element(By.ID, "find_desc")
    location_field = driver.find_element(By.ID, "search_location")
    print("Located search fields")

    time.sleep(5)

    search_field.clear()
    search_field.send_keys("veterinaries")
    location_field.send_keys(Keys.CONTROL + "a")
    location_field.send_keys(Keys.DELETE)
    location_field.send_keys("Los Angeles, CA")
    print("Inputted keywords")
    time.sleep(5)

    location_field.send_keys(Keys.RETURN)
    print("Entered values")
    time.sleep(10)

    companies_written = 0
    while True:
        company_elements = driver.find_elements(By.CSS_SELECTOR, "div.container__09f24__21w3G")

        for company_element in company_elements:
            if companies_written >= 50:
                break

            try:
                link = company_element.find_element(By.CSS_SELECTOR, "a.css-1422juy")
                driver.execute_script("arguments[0].click();", link)
                time.sleep(5)

                extract_and_write_data(driver, sheet)
                companies_written += 1

                driver.back()
                time.sleep(5)
            except Exception as e:
                continue

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a.next-link.navigation-button__09f24__F_sB2")
            next_button.click()
            time.sleep(10)
        except Exception as e:
            break

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    workbook.save("Veterinaries_in_LA.xlsx")
    driver.quit()
    print("Process completed and browser closed")
