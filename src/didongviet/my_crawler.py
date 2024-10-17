from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os, sys, time, datetime, re, json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from env import DATA_DIR
from logging_config import setup_logging

today = datetime.datetime.today().strftime("%Y-%m-%d")
logger = setup_logging(os.path.join(DATA_DIR, "logging.txt"))

def crawl_didongviet():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)

    # Send request
    logger.info("Crawling Di Dong Viet...")
    url = 'https://didongviet.vn/apple-macbook-imac.html'
    driver.get(url)

    # Let the page load fully
    time.sleep(4)

    # Scrolling
    body = driver.find_element(By.TAG_NAME, "body")
    for i in range(2):
        logger.info("> Scrolling ...")
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)

        button = driver.find_element(By.CSS_SELECTOR, ".flex.items-center.justify-center.py-2:nth-child(1)")

        button.click()
        logger.info("> Clicked")

        time.sleep(2)

    # Check how many items to crawl
    items = driver.find_elements(By.XPATH, "//div[@class='_loading_overlay_wrapper css-79elbk']/div/div")
    logger.info(f"Number of items {len(items)} to crawl")

    DATA = []
    
    # go through each item
    for i in range(1, len(items) + 1, 1):
        temp = {}
        product_name = driver.find_element(By.XPATH, f"//div/div[3]/div/div[3]/div/div[{i}]/a/div[2]/div[2]/h3").text
        price = driver.find_element(By.XPATH, f"//div/div[3]/div/div[3]/div/div[{i}]/a/div[2]/div[3]/div/div[1]/p").text
        product_url = driver.find_element(By.XPATH, f"//div/div[3]/div/div[3]/div/div[{i}]/a").get_attribute('href')

        if "MacBook" in product_name:
            # regex
            mac_type = re.findall("Air|Pro", product_name)[0]
            screen_size = re.findall("13|14|15|16", product_name)[0]
            ram = re.findall("8GB|16GB|18GB|36GB|48GB", product_name)[0]
            ssd = re.findall("256GB|512GB|1TB", product_name)[0]
            chipset = re.findall("M1|M2|M3", product_name)[0]
            date = today

            # store in temp dict
            temp["date"] = today
            temp["store"] = "di-dong-viet"
            temp["product_name"] = product_name
            temp['screen_size'] = screen_size + " inch"
            temp['chipset'] = chipset
            temp['ram'] = ram
            temp['ssd'] = ssd
            temp['price'] = price.replace(".", "").replace(" đ", "")
            temp['url'] = product_url

            DATA.append(temp)

    with open(os.path.join(DATA_DIR, f"di_dong_viet/daily_parsed/{today}.json"), "w") as f:
        json.dump(DATA, f, indent=2)
    logger.info("> Crawled data from Di Dong Viet")

if __name__ == "__main__":
    crawl_didongviet()


