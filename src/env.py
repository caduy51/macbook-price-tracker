import os
import sys

src_dir = os.path.dirname(__file__)

PROJECT_DIR = os.path.abspath(os.path.join(src_dir, '..'))

DATA_DIR = os.path.join(PROJECT_DIR, "data")

if __name__ == "__main__":
    print(PROJECT_DIR)
    print(DATA_DIR)

