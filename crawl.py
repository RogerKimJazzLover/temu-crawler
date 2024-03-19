import time
from browser import Browser
from bs4 import BeautifulSoup as bs

def extract_text(arr:list,keyword:str) -> list:
    res = []
    if keyword=="text":
        for i in range(len(arr)):
            res.append(arr[i].get_text())
        return res
    for j in range(len(arr)):
        res.append(arr[j][keyword])
    return res

def main():
    brsr = Browser()    
    brsr.goToPage("https://www.temu.com/kr/channel/best-sellers.html")
    page = brsr.getPageSource() 
    soup = bs(page, "html.parser")

    #Using user-agent
    raw_arr = []
    filtered_data = soup.find_all("div", attrs={"class":"list-3U7_4"}) #data-tooltip-title
    pretty = filtered_data[0].prettify()
    for i in range(1,21):
        prd = soup.find_all("div", attrs={"data-uniqid":str(i)})
        raw_arr.append(prd)
    
    #40 items
    # titles = soup.find_all("div", attrs={"class":"_6q6qVUF5 _1UrrHYym", "data-tooltip-fixed":"false" ,"data-tooltip-hidden":"false"}) #data-tooltip-title
    # rate = soup.find_all("div", attrs={"class":"WCDudEtm _2JVm1TM2", "role":"link"})#arai-label
    # sales_num = soup.find_all("span", attrs={"class":"_1GKMA1Nk _3ByJ_6zs", "data-type":"saleTips"})#arai-label
    # prices = soup.find_all("span", attrs={"aria-hidden":"true", "class":"LiwdOzUs"}) #text
    # rate_num = soup.find_all("span", attrs={"class":"_3CizNywp"}) #text

    products = {
        "titles":titles,
        "rate":rate,
        "sales_num":sales_num,
        "prices":prices,
        "rate_num":rate_num,
    }

    for key, value in products.items():
        # print(len(value))
        if key == "titles":
            res = extract_text(value, "data-tooltip-title")
            products[key] = res
        elif key == "rate" or key == "sales_num":
            res = extract_text(value, "aria-label")
            products[key] = res
        else:
            res = extract_text(value, "text")
            products[key] = res

    brsr.driver.quit()

if __name__ == "__main__":
    main()