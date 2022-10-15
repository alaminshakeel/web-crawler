from multiprocessing import Lock, Process, Queue, current_process
import time
import queue # imported for using queue.Empty exception

import sys
# from dotenv import load_dotenv
# from pathlib import Path
from classes import *

def main():
    number_of_processes = 10
    processes = []

    # "https://cosmeet.cosme.net/product/search/page/1/srt/4/itm/800/disps/2"
    BASE_URL = 'https://cosmeet.cosme.net'
    QUERY_STRING = '/product/search/page/{}/srt/4/itm/{}/disps/2'
    TOTAL_PRODUCTS = -1
    PRODUCTS_PER_PAGE = 10
    # CATEGORY_IDS = [800, 803]
    FROM = 1
    TO = 101
    # FILE_NAME = 1

    try:
        CATEGORY = int(sys.argv[1])
        FROM = int(sys.argv[2])
        TO = int(sys.argv[3])
        # PART = sys.argv[2]

    except:
        pass

    # crawl products
    crawler = Crawler(BASE_URL, QUERY_STRING, TOTAL_PRODUCTS, PRODUCTS_PER_PAGE, CATEGORY, FROM, TO)
    # crawler.collect_product_list()

    # creating processes
    # offset = 1000
    number_of_processes = 4
    offset = (TO // number_of_processes) + 1
    for w in range(1, number_of_processes+1):
        # offset = TO//number_of_processes

        b_from, b_to = (offset*(w-1)) + 1, offset*w if offset*w <= TO else TO
        print(b_from, b_to)
        p = Process(target=crawler.collect_product_list, args=(CATEGORY, b_from, b_to, w))
        processes.append(p)
        p.start()

    # completing process
    for p in processes:
        p.join()

    # print the output

    # while not tasks_that_are_done.empty():
    #     print(tasks_that_are_done.get())

    return True


if __name__ == '__main__':
    main()
