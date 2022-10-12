import os

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import math


class Selenium:

    def __init__(self):
        file_dir = os.path.dirname(os.path.realpath(__file__))
        self.driver_path = os.path.join(file_dir, 'chromedriver')

    def get_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        return Chrome(executable_path=self.driver_path, options=chrome_options)


class Crawler:

    def __init__(self, base_url, query_string, total_items_to_crawl, items_per_page, category_ids):
        self.item_urls = set()
        self.products_data = []
        self.base_url = base_url
        self.query_string = query_string
        self.total_items_to_crawl = total_items_to_crawl
        self.items_per_page = items_per_page
        self.category_ids = category_ids
        self.selenium = Selenium()

    def total_page_to_crawl(self):

        self.driver = self.selenium.get_driver()
        self.driver.get(self.full_path)
        pagination_text = self.driver.find_elements(By.XPATH, '//div[@id="keyword-product"]/div[@class="cmn-paging clearfix"]/p')[0]
        self.total_items_to_crawl = int(pagination_text.text.split("件中")[0])
        print(self.total_items_to_crawl)
        return math.ceil(int(self.total_items_to_crawl) / int(self.items_per_page)) + 1

    def get_category_ids(self):
        return self.category_ids

    def collect_product_list(self):
        for category_id in self.get_category_ids():

            self.full_path = self.base_url + self.query_string.format(category_id, 1)
            print(self.full_path)
            self.driver = self.selenium.get_driver()
            self.driver.get(self.full_path)

            try:
                WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cmn-paging"))
                )
            except:
                pass

            self.driver.quit()
            for page in range(1, self.total_page_to_crawl()):

                self.full_path = self.base_url + self.query_string.format(category_id, page)
                print(self.full_path)
                self.driver = self.selenium.get_driver()
                self.driver.get(self.full_path)

                elems = self.driver.find_elements(By.XPATH, '//div[@id="keyword-product-list"]/div/div/div/h3/a[@href]')
                for elem in elems:
                    self.item_urls.add(elem.get_attribute("href"))




    def scrape_product_contents(self):
        all_SN = []
        all_breadcrumbs = []
        all_product_urls = []
        all_captions = []
        all_product_names = []
        all_product_ids = []
        all_keywords = []
        all_prices = []
        all_features = []
        all_colors = []
        all_sizes = []
        all_descriptions = []
        all_functions = []
        all_materials = []
        all_weights = []
        all_image_urls = []
        all_image_urls_by_variants = []
        all_review_scores = []
        all_number_of_reviews = []
        all_review_details = []
        all_products_tags = []

        all_3xs_sizes = []
        all_2xs_sizes = []
        all_xs_sizes = []
        all_s_sizes = []
        all_m_sizes = []
        all_l_sizes = []
        all_xl_sizes = []
        all_xxl_sizes = []

        all_36_sizes = []
        all_38_sizes = []
        all_40_sizes = []
        all_42_sizes = []

        for sn, item_url in enumerate(self.item_urls):
            all_SN.append(sn+1)
            self.driver = self.selenium.get_driver()
            self.driver.get(item_url)
            try:
                WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "productPlainImage_custom"))
                )
            except:
                pass

            """
            breadcrumbs
            """
            elems = self.driver.find_elements(By.XPATH, '//li[@class="fs-c-breadcrumb__listItem"]/a[@href]')
            breadcrumbs_items = []
            for elem in elems:
                breadcrumbs_items.append(elem.text)
            all_breadcrumbs.append(" / ".join(breadcrumbs_items))

            """
            product url
            """
            all_product_urls.append(item_url)

            """
            captions
            """
            try:
                el = self.driver.find_element(By.CLASS_NAME, 'fs-c-productNameHeading__copy')
                all_captions.append(el.text)
            except:
                all_captions.append("N/A")

            """
            product name
            """
            try:
                el = self.driver.find_element(By.CLASS_NAME, 'fs-c-productNameHeading__name')
                all_product_names.append(el.text)
            except:
                all_product_names.append("N/A")

            """
            KW
            """
            try:
                els = self.driver.find_elements(By.CLASS_NAME, 'fs-c-productMark__label')
                all_keywords.append(", ".join(list(filter(lambda x: x != "", [el.text.strip() for el in els]))))
            except:
                all_keywords.append("N/A")
            """
            price
            """
            try:
                el = self.driver.find_element(By.CLASS_NAME, 'fs-c-price__value')
                all_prices.append(el.text)
            except:
                all_prices.append(0)

            """
            feature of products
            """
            try:
                el = self.driver.find_element(By.CLASS_NAME, 'fs-p-productDescription--short')
                all_features.append(el.text)
            except:
                all_product_names.append("N/A")

            """
            Colors/Variants
            """
            variants_codes = []
            try:
                els = self.driver.find_elements(By.NAME, 'horizontal-select')
                all_colors.append([
                    {
                        "color_name": el.get_attribute('data-horizontal-variation-name'),
                        "color_code": el.get_attribute('data-horizontal-admin-no').strip("-")
                    }
                    for el in els
                ])

                variants_codes = [el.get_attribute('data-horizontal-admin-no').strip("-") for el in els]

            except:
                all_colors.append([])

            """
            size
            """
            sizes = []
            try:
                els = self.driver.find_elements(By.NAME, 'vertical-select')
                sizes = [el.get_attribute('data-vertical-variation-name') for el in els]
                all_sizes.append(", ".join(sizes))
            except:
                all_sizes.append("")

            """
            product id's
            """
            try:
                el = self.driver.find_element(By.CLASS_NAME, 'fs-c-productNumber__number')
                product_item_code = "-".join(el.text.split("-")[:-2])
                product_ids = list(map(
                    lambda x: "-".join([product_item_code, x]),
                    ["-".join([code, size]) for code in variants_codes for size in sizes]
                )
                )
                all_product_ids.append(", ".join(product_ids))
            except:
                all_product_ids.append("")

            """
            description
            """
            desc_bodies = self.driver.find_elements(By.XPATH,
                                                    '//div[@class="product-description-box"]/p[@class="body"]')
            desc_names = self.driver.find_elements(By.XPATH,
                                                   '//div[@class="product-description-box"]/p[@class="descript-name"]')

            check_desc_sync = self.driver.find_element(By.XPATH, '//div[@class="product-description-box"]')
            desc_sync = check_desc_sync.text.split("装備")[0].strip()
            body_sync = desc_bodies[0].text.strip()

            if desc_sync.split("。")[0] == body_sync.split("。")[0]:
                from_start = 1
            else:
                from_start = 0

            all_descriptions.append(desc_sync)

            functions_txt = "N/A"
            for i, name in enumerate(desc_names, from_start):
                # function
                if name.text.strip() == "装備":
                    functions_txt = desc_bodies[i].text
                    break
            all_functions.append(functions_txt)

            material_text = "N/A"
            for i, name in enumerate(desc_names, from_start):
                # material
                if name.text.strip() == "素材":
                    material_text = desc_bodies[i].text
                    break
            all_materials.append(material_text)

            weight_text = "N/A"
            for i, name in enumerate(desc_names, from_start):
                # weight
                if name.text.strip() == "重量":
                    weight_text = desc_bodies[i].text
                    break
            all_weights.append(weight_text)

            """
            size chart
            """
            _36_sizes = "{}"
            _38_sizes = "{}"
            _40_sizes = "{}"
            _42_sizes = "{}"

            _3xs_sizes = "{}"
            _2xs_sizes = "{}"
            _xs_sizes = "{}"
            _s_sizes = "{}"
            _m_sizes = "{}"
            _l_sizes = "{}"
            _xl_sizes = "{}"
            _xxl_sizes = "{}"

            # pick the table
            try:
                els_ttl = self.driver.find_elements(By.CLASS_NAME, 'size-table-ttl')
                els_data = self.driver.find_elements(By.CLASS_NAME, 'size-table-data')
                els_sku = self.driver.find_elements(By.CLASS_NAME, 'size-table-sku')

                len_ttl = len(els_ttl)-1
                for index, el in enumerate(els_data):
                    if index % len_ttl == 0:
                        size_breakdown = {els_ttl[ind].text: els_data[index + (ind-1)].text for ind in range(1, len(els_ttl))}
                        if els_sku[index // len_ttl].text.strip() == '3XS':
                            _3xs_sizes = size_breakdown
                        elif els_sku[index // len_ttl].text.strip() == '2XS':
                            _2xs_sizes = size_breakdown
                        elif els_sku[index // len_ttl].text.strip() == 'XS':
                            _xs_sizes = size_breakdown
                        elif els_sku[index // len_ttl].text.strip() == 'S':
                            _s_sizes = size_breakdown
                        elif els_sku[index // len_ttl].text.strip() == 'M':
                            _m_sizes = size_breakdown
                        elif els_sku[index // len_ttl].text.strip() == 'L':
                            _l_sizes = size_breakdown
                        elif els_sku[index // len_ttl].text.strip() == 'XL':
                            _xl_sizes = size_breakdown
                        elif els_sku[index // len_ttl].text.strip() == 'XXL':
                            _xxl_sizes = size_breakdown
                        elif els_sku[index // len_ttl].text.strip() == '36':
                            _36_sizes = size_breakdown
                        elif els_sku[index // len_ttl].text.strip() == '38':
                            _38_sizes = size_breakdown
                        elif els_sku[index // len_ttl].text.strip() == '40':
                            _40_sizes = size_breakdown
                        elif els_sku[index // len_ttl].text.strip() == '42':
                            _42_sizes = size_breakdown

            except:
                pass

            all_3xs_sizes.append(_3xs_sizes)
            all_2xs_sizes.append(_2xs_sizes)
            all_xs_sizes.append(_xs_sizes)
            all_s_sizes.append(_s_sizes)
            all_m_sizes.append(_m_sizes)
            all_l_sizes.append(_l_sizes)
            all_xl_sizes.append(_xl_sizes)
            all_xxl_sizes.append(_xxl_sizes)
            all_36_sizes.append(_36_sizes)
            all_38_sizes.append(_38_sizes)
            all_40_sizes.append(_40_sizes)
            all_42_sizes.append(_42_sizes)

            """
            image urls
            """
            all_images = []
            all_unique_images = set()
            try:
                els = self.driver.find_elements(By.XPATH, '//div[@class="horizontal_select_custom"]/label')
                for el in els:
                    el.click()

                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(By.XPATH, '//div[@class="productPlainImage_custom"]/ul/li/img')
                        )
                    except:
                        pass

                    color_info = self.driver.find_element(By.CLASS_NAME, 'color_info').text
                    images = self.driver.find_elements(By.XPATH, '//div[@class="productPlainImage_custom"]/ul/li/img')
                    all_images.append(
                        {
                            "color_info": color_info,
                            "image_links": [image.get_attribute('src') for image in images]
                        }
                    )

                    for image in images:
                        all_unique_images.add(image.get_attribute('src'))
            except:
                pass

            all_image_urls_by_variants.append(all_images)
            all_image_urls.append(list(all_unique_images))

            """
            review score
            """
            try:
                el = self.driver.find_element(By.CLASS_NAME, 'fs-c-rating__value')
                all_review_scores.append(el.text + " / 5.0")
            except:
                all_review_scores.append("0.0 / 5.0")

            """
            number of review
            fs-c-aggregateRating__count
            """
            try:
                el = self.driver.find_element(By.CLASS_NAME, 'fs-c-aggregateRating__count')
                all_number_of_reviews.append(el.text)
            except:
                all_number_of_reviews.append(0)

            """
            details of review
            """
            try:
                els = self.driver.find_elements(By.CLASS_NAME, 'fs-c-reviewList__item')
                review_details = [
                    {
                        "reviewer_name": el.find_element(By.CLASS_NAME, "fs-c-reviewer__name__nickname").text,
                        "review_date": el.find_element(By.CLASS_NAME, "fs-c-time").get_attribute("datetime"),
                        "review_rating": el.find_element(By.CLASS_NAME, "fs-c-reviewInfo__stars").get_attribute("data-ratingcount") + " / 5.0",
                        "review_body": el.find_element(By.CLASS_NAME, "fs-c-reviewList__item__body").text,
                    }
                    for el in els
                ]

                all_review_details.append(review_details)
            except:
                all_review_details.append([])

            """
            product tags
            """
            try:
                els = self.driver.find_elements(By.XPATH,
                                                '//a[@class="sc-bdnxRM isDaSX awoo-tag"]/span')
                all_products_tags.append(", ".join([el.text for el in els]))
            except:
                all_products_tags.append("N/A")

            self.driver.quit()
            print('done..')

        # appending row
        self.products_data = list(zip(
            all_SN,
            all_breadcrumbs,
            all_product_urls,
            all_image_urls,
            all_image_urls_by_variants,
            all_captions,
            all_product_names,
            all_product_ids,
            all_keywords,
            all_prices,
            all_features,
            all_colors,
            all_sizes,
            all_descriptions,
            all_functions,
            all_materials,
            all_weights,

            all_3xs_sizes,
            all_2xs_sizes,
            all_xs_sizes,
            all_s_sizes,
            all_m_sizes,
            all_l_sizes,
            all_xl_sizes,
            all_xxl_sizes,

            all_36_sizes,
            all_38_sizes,
            all_40_sizes,
            all_42_sizes,

            all_review_scores,
            all_number_of_reviews,
            all_review_details,
            all_products_tags
        ))


class Exporter:
    def __init__(self, columns, data):
        self.columns = columns
        self.data = data
        self.to_format = 'xls'

    def save_as(self, file_name):
        df = pd.DataFrame(self.data, columns=self.columns)

        # dataset name & columns names
        df.to_excel('.'.join([file_name, self.to_format]), index=False)
