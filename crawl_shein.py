import time
from collections import Counter

import bs4
from browser import Browser
from bs4 import BeautifulSoup as bs

import pandas as pd
from tabulate import tabulate

def get_repeated_classes(soup) -> dict:
    elements_with_class = soup[0].find_all(class_=True)
    class_names = []
    # Iterate over the elements and add their class names to the list
    # Note: An element can have multiple classes, hence we extend the list
    for element in elements_with_class:
        class_names.extend(element['class'])    

    # Count the occurrences of each class name
    class_name_counts = Counter(class_names)    

    # Filter class names that repeat (appear more than once)
    repeating_class_names = {class_name: count for class_name, count in class_name_counts.items() if count > 1} 

    return repeating_class_names

def get_element_with_repeated_clases(repeated_classes: dict, filtered_data: bs4.element.ResultSet):
    elements = repeated_classes
    for key, value in elements.items():
        element = filtered_data[0].find_all(attrs={"class":key})
        elements[key] = element
    '''
    쓸모있는 class 명:
    Mobile:
        1. price
        2. title
        3. rank-product-item__r
        4. item-r__t
        5. rank-product-item
    PC:
        1. S-product-item__price
        2. S-product-item__name
    '''
    return elements

def extract_text(code: str) -> str:
    '''
    Takes a raw html code, with one string
    Then return the natural language part
    '''
    # code = bs(code, "html.parser")
    return code.get_text()

def main():
    brsr = Browser()    
    brsr.goToPage("https://asia.shein.com/campaigns/mostpopularitems")
    brsr.scrollPageToBottom()
    brsr.clickButton("/html/body/div[1]/div[1]/div/div/div/div[4]/button")
    time.sleep(1)

    for _ in range(50):
        brsr.scrollPageToBottom()
        time.sleep(0.5)
    page = brsr.getPageSource() 
    soup = bs(page, "html.parser")
    brsr.driver.quit()

    # FILTERING STEP 1. "Getting the divs"
    filtered_data = soup.find_all("div", attrs={"class":"product-list"})
    repeated_classes = get_repeated_classes(soup=filtered_data)
    elements = get_element_with_repeated_clases(repeated_classes, filtered_data)
    # For mobile: desired_keys = ['price', 'title', 'rank-product-item__r', 'item-r__t', 'rank-product-item']
    desired_keys = ["S-product-item__price", "S-product-item__name"]
    elements = {key: elements[key] for key in desired_keys}
    
    # FILTERING STEP 2. "Getting the text"
    for key, value in elements.items():
        arr = []
        for i in range(len(value)):
            arr.append(extract_text(value[i]))
        elements[key] = arr

    #Defining data for csv
    elements = pd.DataFrame(elements)
    elements.rename(columns = {'S-product-item__price' : '가격', 'S-product-item__name' : '상품명'}, inplace = True)
    elements.to_csv("./data/shein_most_popular_item.csv", encoding="utf-16", index=False)
    # print(tabulate(elements, headers='keys', tablefmt='psql'))

if __name__ == "__main__":
    main()