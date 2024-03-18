from browser import Browser

def main():
  brsr = Browser("/usr/bin/chromedriver")

  brsr.goToPage("https://www.temu.com/kr/channel/best-sellers.html")
  page = brsr.getPageSource()

  return 0

if __name__ == "__main__":
  main()