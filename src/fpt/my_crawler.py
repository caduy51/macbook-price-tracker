from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os, sys, re, json, time, datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from env import DATA_DIR
from logging_config import setup_logging

today = datetime.datetime.today().strftime("%Y-%m-%d")
logger = setup_logging(os.path.join(DATA_DIR, "logging.txt"))

def crawl_fpt():
    # Set up Chrome WebDriver options (optional)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (without opening a browser window)

    driver = webdriver.Chrome(options=chrome_options)

    # Send request
    logger.info("Crawling FPT Shop ...")
    url = 'https://fptshop.com.vn/may-tinh-xach-tay/apple-macbook' 
    driver.get(url)

    # Let the page load fully
    time.sleep(2)

    # Scrolling
    body = driver.find_element(By.TAG_NAME, "body")
    for i in range(3):
        body.send_keys(Keys.PAGE_DOWN)
        logger.info("> Scrolling ...")
        time.sleep(1)

    # Click buttons
    button = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div[2]/div[3]/div[3]/button")
    button.click()
    logger.info("> Clicked")
    time.sleep(1)

    # Check how many items to crawl
    items = driver.find_elements(By.XPATH, "//div[@class='grid grid-cols-2 gap-2 md:grid-cols-4']/div")
    logger.info(f"Number of items {len(items)} to crawl")

    DATA = []
    # go through each item
    for i in range(1, len(items) + 1, 1):
        temp = {}
        try:
            price = driver.find_element(By.XPATH, f"//div[{i}]/div/div[2]/div[1]/p[2]").text.replace(" ₫", "").replace(".", "")
        except NoSuchElementException:
            price = driver.find_element(By.XPATH, f"//div[{i}]/div/div[2]/div[1]/p").text.replace(" ₫", "").replace(".", "")

        product_name = driver.find_element(By.XPATH, f"//div[{i}]/div/div[2]/h3/a").text
        product_url = driver.find_element(By.XPATH, f"//div[{i}]/div/div[2]/h3/a").get_attribute("href")
        mac_type = re.findall("Air|Pro", product_name)[0]
        screen_size = re.findall("13|14|15|16", product_name)[0]
        ram = re.findall("8GB|16GB|18GB|36GB|48GB", product_name)[0]
        ssd = re.findall("256GB|512GB|1TB", product_name)[0]
        chipset = re.findall("M1|M2|M3", product_name)[0]
        date = today

        # Store in temp dict
        temp["date"] = today
        temp["store"] = "fpt-shop"
        temp["product_name"] = product_name
        # temp['mac_type'] = mac_type
        temp['screen_size'] = screen_size + " inch"
        temp['chipset'] = chipset
        temp['ram'] = ram
        temp['ssd'] = ssd
        temp['price'] = price
        temp['url'] = product_url

        DATA.append(temp)

    # Saved to file 
    with open(os.path.join(DATA_DIR, f"fpt_shop/daily_parsed/{today}.json"), "w") as f:
        json.dump(DATA, f, indent=2)

    logger.info("> Crawled data from FPT Shop")

    driver.close()

if __name__ == "__main__":
    crawl_fpt()

