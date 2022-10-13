import sys
from dotenv import load_dotenv
from pathlib import Path
from classes import *

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


if __name__ == "__main__":
    BASE_URL = os.getenv('BASE_URL', 'https://www.millet.jp')
    QUERY_STRING = os.getenv('QUERY_STRING', '/p/search?page={}')
    TOTAL_PRODUCTS = os.getenv('TOTAL_PRODUCTS', 300)
    PRODUCTS_PER_PAGE = os.getenv('PRODUCTS_PER_PAGE', 30)
    CATEGORY_IDS = [800, 803]
    FROM = 1
    TO = 300
    FILE_NAME = 1

    try:
        FROM = sys.argv[1]
        TO = sys.argv[2]
    except:
        pass

    # crawl products
    crawler = Crawler(BASE_URL, QUERY_STRING, TOTAL_PRODUCTS, PRODUCTS_PER_PAGE, CATEGORY_IDS, FROM, TO, FILE_NAME)
    crawler.collect_product_list()





    # scrape products info
    # crawler.scrape_product_contents()




"""
proc:
cosme.com

#steps:
    - list of cat = []
    - loop through cats
        - get last page no
        - brows through the page no
            - fetch the product urls
            - 


#goal
scrap all product urls

"""
