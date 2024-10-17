from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time, sys, os

# Set up Chrome WebDriver options (optional)
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (without opening a browser window)

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Send request
url = 'https://cellphones.com.vn/laptop/mac.html' 
driver.get(url)

# Let the page load fully
time.sleep(2)

# Click buttons
button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div[2]/div/div[4]/div[5]/div/div[2]/a")
button.click()
print("Clicked more")
time.sleep(3)
button.click()
print("Clicked more")
time.sleep(3)
button.click()
print("Clicked more")
time.sleep(3)
button.click()
print("Clicked more")
time.sleep(3)

items = driver.find_elements(By.XPATH, "//div[@class='product-info-container product-item']")
print(f"Number of items {len(items)}")

macbook_urls = []

# Extract item url
for i in range(1, len(items) + 1, 1):
    url = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[3]/div[2]/div/div[4]/div[5]/div/div[1]/div[{i}]/div[1]/a').get_attribute('href')
    if "macbook" in url:
        macbook_urls.append(url)

print(f"Number of macbooks {len(macbook_urls)}")

# Go through each item url
for macbook_url in macbook_urls[:5]:
    driver.get(macbook_url)
    boxes = driver.find_elements(By.XPATH, "//div[@class='list-linked']/a")

    for box in boxes:
        try:
            info_1 = box.find_element(By.XPATH, ".//strong[1]").text
        except NoSuchElementException:
            info_1 = None
        
        try:
            info_2 = box.find_element(By.XPATH, ".//strong[2]").text
        except NoSuchElementException:
            info_2 = None

        try:
            info_3 = box.find_element(By.XPATH, ".//strong[3]").text
        except NoSuchElementException:
            info_3 = None
        
        try:
            info_4 = box.find_element(By.XPATH, ".//span").text
        except NoSuchElementException:
            info_4 = None
        
        print(f"{macbook_url}, {info_1}, {info_2}, {info_3}, {info_4}")

driver.close()


