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

    # crawl products
    crawler = Crawler(BASE_URL, QUERY_STRING, TOTAL_PRODUCTS, PRODUCTS_PER_PAGE)
    crawler.collect_product_list()

    # scrape products info
    crawler.scrape_product_contents()

    headers = [
        "S/L", "Breadcrumbs", "Product URL", "All Images",
        "Color wise images", "Caption", "Product Name", "Product Ids",
        "KWs", "Price", "Feature", "Colors", "Sizes", "Description",
        "Function", "Material", "Weight", "Size - 3XS", "Size - 2XS",
        "Size - XS", "Size - S", "Size - M", "Size - L", "Size - XL",
        "Size - XXL", "Size - 36", "Size - 38", "Size - 40", "Size - 42",
        "Review Score", "No of Reviews", "Review details", "Tags"
    ]

    # export
    exporter = Exporter(headers, crawler.products_data)
    exporter.save_as('products_info')