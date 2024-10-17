import os 
import json
from env import DATA_DIR
from time import sleep
from logging_config import setup_logging

logger = setup_logging(os.path.join(DATA_DIR, "logging.txt"))

def extract_from_files():
    stores = ["the_gioi_di_dong", "fpt_shop", "di_dong_viet"]
    logger.info(f"Reading files from {stores}")

    data = []

    # Merging
    for store in stores:
        store_dir = os.path.join(DATA_DIR, f"{store}/daily_parsed")
        file_names = os.listdir(store_dir)
        logger.info(f"{store_dir}, {file_names}")

        # Loops through files, read, load
        for file_name in file_names:
            if ".json" in file_name:
                with open(os.path.join(store_dir, file_name), "r") as f:
                    file_data = json.load(f)
                    for record in file_data:
                        data.append(record)
        sleep(0.5)

    # Write back to File System
    with open(os.path.join(DATA_DIR, "output/output.json"), "w") as f:
        json.dump(data, f, indent=2)
        
    logger.info("> Merged All Files. OK")

if __name__ == "__main__":
    extract_from_files()


