import requests
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from env import DATA_DIR
from logging_config import setup_logging

def crawl_tgdd():
    # Set up Logger
    logger = setup_logging(os.path.join(DATA_DIR, "logging.txt"))
    
    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

    urls = ["https://www.thegioididong.com/laptop-air",
            "https://www.thegioididong.com/laptop-pro"]

    for url in urls:
        logger.info("Crawling The gioi di dong ...")
        # Send requests
        response = requests.get(url, headers=HEADERS)
        category_name = url.split("/")[-1]
        if response.status_code == 200:
            data = response.text
            # Save into file
            with open(os.path.join(DATA_DIR, f"the_gioi_di_dong/html/{category_name}.html"), "w") as f:
                f.write(data)
            logger.info(f"> Saved '{category_name}' into html. OK")
        else:
            print(response.status_code)

if __name__ == "__main__":
    crawl_tgdd()







