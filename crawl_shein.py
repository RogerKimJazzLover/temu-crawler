import bs4
import time
from browser import Browser
from collections import Counter
from bs4 import BeautifulSoup as bs

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
    return elements

def main():
    brsr = Browser()    
    brsr.goToPage("https://asia.shein.com/campaigns/mostpopularitems")
    page = brsr.getPageSource() 
    soup = bs(page, "html.parser")
    print(type(soup))

    # filtered_data = soup.find_all("div", attrs={"infinite-scroll-disabled":"scrollDisabled"})
    filtered_data = soup.find_all("ul", attrs={"class":"list-block"})
    print(type(filtered_data))
    print(type(filtered_data[0]))
    repeated_classes = get_repeated_classes(soup=filtered_data)
    elements = get_element_with_repeated_clases(repeated_classes, filtered_data)

    brsr.driver.quit()

if __name__ == "__main__":
    main()