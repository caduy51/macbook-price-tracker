from lxml import etree 
from datetime import date
import os, sys, re, json, time, datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from env import DATA_DIR
from logging_config import setup_logging

# Set up logger
logger = setup_logging(os.path.join(DATA_DIR, "logging.txt"))

today = datetime.datetime.today().strftime("%Y-%m-%d")
html_files = ["laptop-air.html", "laptop-pro.html"]

def parse_tgdd():
    data = []

    for html_file in html_files:
        logger.info(f"Parsing {html_file}")
        with open(os.path.join(DATA_DIR, f"the_gioi_di_dong/html/{html_file}"), "r") as f:
            html = f.read()
            parser = etree.HTMLParser()
            root = etree.fromstring(html, parser)

            ul_element = root.xpath('//ul[@class="listproduct"]')[0]
            num_products = len(ul_element.getchildren())

            for i in range(1, num_products + 1, 1):
                temp = {}
                product_name = root.xpath(f"//ul[@class='listproduct']/li[{i}]/a/h3/text()")[0].strip()
                ram = root.xpath(f"//ul[@class='listproduct']/li[{i}]/a/div[3]/span[1]/text()")[0].replace("RAM", "").strip().replace(" ", "")
                ssd = root.xpath(f"//ul[@class='listproduct']/li[{i}]/a/div[3]/span[2]/text()")[0].replace("SSD", "").strip().replace(" ", "")
                price = root.xpath(f"//ul[@class='listproduct']/li[{i}]/a/strong/text()")[0].strip().replace("₫", "").replace(".", "")
                product_url = root.xpath(f"//ul[@class='listproduct']/li[{i}]/a[1]/@href")[0]

                # regex
                screen_size = re.findall("\d{2} inch", product_name)[0]
                chipset = re.findall("M\d{1}", product_name)[0]

                # create a temp dict
                temp['date'] = today
                temp['store'] = "the-gioi-di-dong"
                temp['product_name'] = product_name
                temp['screen_size'] = screen_size
                temp['chipset'] = chipset
                temp['ram'] = ram
                temp['ssd'] = ssd
                temp['price'] = price
                temp['url'] = "https://www.thegioididong.com" + product_url
                data.append(temp)

    # Saved parsed data
    with open(os.path.join(DATA_DIR, f"the_gioi_di_dong/daily_parsed/{today}.json"), "w") as f:
        json.dump(data, f, indent=2)

    logger.info("> Write Json File. OK")

if __name__ == "__main__":
    parse_tgdd()

            




