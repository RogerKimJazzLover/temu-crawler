import time
from browser import Browser
from bs4 import BeautifulSoup as bs

def main():
    brsr = Browser()    
    brsr.goToPage("https://asia.shein.com/campaigns/mostpopularitems")
    page = brsr.getPageSource() 
    soup = bs(page, "html.parser")

    brsr.driver.quit()

if __name__ == "__main__":
    main()