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

    # crawl products
    crawler = Crawler(BASE_URL, QUERY_STRING, TOTAL_PRODUCTS, PRODUCTS_PER_PAGE, CATEGORY_IDS)
    crawler.collect_product_list()

    # scrape products info
    # crawler.scrape_product_contents()

    headers = [
        "Product URL"
    ]
    # "S/L", "Breadcrumbs", "Product URL", "All Images",
    # "Color wise images", "Caption", "Product Name", "Product Ids",
    # "KWs", "Price", "Feature", "Colors", "Sizes", "Description",
    # "Function", "Material", "Weight", "Size - 3XS", "Size - 2XS",
    # "Size - XS", "Size - S", "Size - M", "Size - L", "Size - XL",
    # "Size - XXL", "Size - 36", "Size - 38", "Size - 40", "Size - 42",
    # "Review Score", "No of Reviews", "Review details", "Tags"
    print(crawler.item_urls)
    # export
    exporter = Exporter(headers, crawler.item_urls)
    # exporter = Exporter(headers, crawler.products_data)
    exporter.save_as('products_info')


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