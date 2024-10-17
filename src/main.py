#!/Users/admin/opt/anaconda3/bin/python

from didongviet.my_crawler import crawl_didongviet
from fpt.my_crawler import crawl_fpt
from tgdd.my_crawler import crawl_tgdd
from tgdd.my_parser import parse_tgdd
from extract import extract_from_files
from load import load_to_sheets

if __name__ == "__main__":
    # Run crawler
    crawl_tgdd()
    parse_tgdd()
    crawl_fpt()
    crawl_didongviet()
    # ETL process
    extract_from_files()
    load_to_sheets()
    





