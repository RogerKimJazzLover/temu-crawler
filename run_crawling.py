from datetime import datetime, timedelta
# from tqdm import trange
import os
import pandas as pd
import time

from shein_crawler import SheinCrawler

def main():
    i = 0
    con = 'y'
    crawler = SheinCrawler()
    while i < 32 and con == 'y':
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        tomorrow = tomorrow.replace(hour=0, minute=0, second=5, microsecond=0)
        start_date = now.date()

        time_til_tmr = (tomorrow - datetime.now()).total_seconds()
        if time_til_tmr < 61:
            print(f"\nSYSTEM: Time left until tommorrow {time_til_tmr} seconds. Proceed to continue after {time_til_tmr} seconds")
            time.sleep(time_til_tmr)
            continue
        else:
            soup = crawler.get_page_source()
            elements = crawler.filter_data(soup)
            crawler.save_to_csv(elements, str(start_date))
            time.sleep(time_til_tmr)
        i += 1
        con = input("Do you want to continue collecting? [y/n]")

if __name__ == "__main__":
    main()