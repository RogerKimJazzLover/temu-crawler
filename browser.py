from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_stealth import stealth

import time

class Browser:
    def __init__(self):
        self.user_agents = [
            #Mobile
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
            #PC
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        ]
        self.driver = self.createStealthDriver()

        self.waitTime = 0.5 # wait 1 second for loading
        self.urlList = []

    def createStealthDriver(self):
        chrome_options = Options()        
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        # chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=chrome_options)

        stealth(
            driver=driver,
            user_agent= self.user_agents[1],
            languages=["ko"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        return driver
        
    def goToPage(self,url):
        self.driver.get(url)
    
    def getPageSource(self):
        return self.driver.page_source

    def clickButton(self, x_path: str):
        button = self.driver.find_element(By.XPATH, x_path)
        button.click()

    # def expandComments(self):
    #     try:
    #         # loading all comments.
    #         # if all comments is loaded, exception will raise on click function
    #         while(True):
    #             expandScript = "return (a = document.getElementsByClassName('Z4IfV')[0].click())"
    #             self.driver.execute_script(expandScript)
    #             time.sleep(0.1)
    #     except:
    #         pass
    
    def getPageSourceCond(self, element):
        delay = 30
        myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, element)))
        return self.getPageSource()

    def scrollPageToBottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def getLinkSize(self):
        return len(self.urlList)

    def clearLink(self):
        self.urlList = []
        
    def scrollPageToBottomUntilEnd(self, mFunc, limitNum):
        dup = 0
        while True:
            self.scrollPageToBottom()
            curSource = self.getPageSource()
            time.sleep(self.waitTime)
            mFunc(curSource)
            nextSource = self.getPageSource()
            # check url link size is limitNum
            if limitNum > 0 and self.getLinkSize() >= limitNum:
                self.urlList = self.urlList[:limitNum]
                break
            # check for end
            if len(curSource) == len(nextSource):
                dup += 1
            else:
                dup = 0
            # retry three more time 
            if dup > 2:
                break
        
    # def collectDpageUrl(self, data):
    #     r = data.split(f'href="/{self.username}/reel/')[1:]
    #     for i in r:
    #         dPageLink = "https://www.instagram.com/reel/"+i.split('"')[0]+"?hl=en"
    #         if dPageLink not in self.urlList:
    #             self.urlList.append(dPageLink)
            
    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass