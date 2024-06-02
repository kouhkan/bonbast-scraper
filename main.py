from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class BonbastScraper:
    def __init__(self):
        self.driver = self.init_driver()

    @staticmethod
    def init_driver():
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    def extract(self) -> dict:
        self.driver.get("https://www.bonbast.com")
        html_page = self.driver.page_source
        soup = BeautifulSoup(html_page, "html.parser")
        currencies = soup.findAll("table", {"class": "table table-condensed"})
        data = {}

        for c in currencies:
            for row in c.findAll("tr"):
                cells = row.findAll("td")
                if len(cells) == 4:
                    code = cells[0].text.strip()
                    sell = cells[2].text.strip()
                    buy = cells[3].text.strip()
                    data[code] = [sell, buy]
        return data


if __name__ == "__main__":
    bonbast = BonbastScraper()
    print(bonbast.extract())
