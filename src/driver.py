from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
import json
from item import item as it
import Common as c
import time

"""
    The driver class handles all functions related to crawling the webpage
"""
class Driver:

    #Opens the json file that contains links
    def open_json(self) -> dict:
        config = None
        try:
            with open('config.json', 'r') as config_json:
                config = json.load(config_json)
                return config
        except Exception:
            c.error("Critical", "There was a problem with the json file")

        #Sets all of the driver attributes and calls the init functions
    def __init__(self, driver_type, category):
        self.driver = self.init_driver(driver_type)
        self.link = ""
        self.pages = 0
        #The type category items you are trying to scrape (all, skins, crates, ect.)
        self.category = category
        #Adjusts the delay between making requests (needs to be longer if elements don't load)
        self.delay = 15
        self.items =[]
        self.json = self.open_json()
        self.retries = 0

        #Initializes the Selenium webdriver and its options
    def init_driver(self, driver_type):
        chrome_option = Options()
        chrome_option.add_argument("--start-minimized")
        if driver_type == 'chrome':
            return webdriver.Chrome(options=chrome_option)
        else:
            c.error("Critical", "Invalid driver type (Must use chrome)")

        #Sets up the driver to crawl the pages
    def setup_driver(self, type):
        self.set_link(self.build_link(type))
        self.set_pages(self.find_page_total())
        self.driver.get(self.link)

        #Finds the total number of pages for the section
    def find_page_total(self) -> int:
        self.driver.get(self.link)
        wait = WebDriverWait(self.driver, 10)
        total_pages = wait.until(EC.presence_of_element_located((By.ID, 'searchResults_total')))
        total_pages_int = int(round(float(total_pages.text.replace(",", ""))))
        return total_pages_int
    
        #Builds the link for given type of items
    def build_link(self, link_type) -> str:
        collections = self.json["collections"]
        link = ""
        link += self.json["base"]
        try:
            link += collections[link_type]
        except KeyError:
            c.error("moderate", f"The link for {link_type} cannot be found.\n")
            return "LINK ERROR"
        link += self.json["end"]
        return link
    
    #Crawls over the pages and collects the items
    def crawl_pages(self, link_type) -> list[WebElement]:
        self.set_category(link_type)
        self.setup_driver(link_type)
        for i in range(self.pages):
            results = self.collect_webelements()
            name_elem, prices_elem, quan_elem = results
            self.create_items(name_elem, prices_elem, quan_elem)
            time.sleep(self.delay)
            self.page_advance()
    
    #Creates the item containers from the seperate lists
    def create_items(self, names:list[WebElement], prices:list[WebElement], quans:list[WebElement]):
        for i in range(len(names)):
            name = names[i].text
            form_price = c.fix_prices(prices)
            quan = quans[i].text
            _type = c.extract_item_type(name)
            skin = c.extract_skin(name)
            price = form_price[i]
            wear = c.extract_wear(name)
            stat = c.extract_stattrack(name)
            souvenir = c.extract_souvenir(name)
            item = it(_type, skin, price, quan, wear, stat, souvenir)
            self.items.append(item)

    #Finds the next button and advances to the next page
    def page_advance(self):
        next_button = self.driver.find_element(By.ID, 'searchResults_btn_next')
        next_button.click()

    #Collects the item information and stores them in the respective list
    def collect_webelements(self) -> tuple[WebElement, WebElement, WebElement]:
        names = None
        prices = None
        quantities = None

        #Retry locating the elements on the webpage
        for _ in range(5):  # Retry up to 5 times
            try:
                names = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'market_listing_item_name'))
                )
                prices = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'normal_price'))
                )
                quantities = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'market_listing_num_listings_qty'))
                )
                # If elements are located successfully, break out of the loop
                break
            except Exception:
                c.error("moderate", "Could not locate web elements. Retrying...\n")
                self.retries += 1
                if self.retries < 5:
                    time.sleep(self.delay)
                else:
                    c.error("critical", "Could not locate the web elements after 5 retries\n")
                    return None, None, None
            finally:
                self.retries = 0  # Reset retries counter

        return names, prices, quantities

    
#---------------------------- Getters and Setters --------------------------------------
    def get_pages(self):
        return self.pages
    
    def set_pages(self, value):
        self.pages = value
    
    def get_link(self):
        return self.link
    
    def set_link(self, link):
        self.link = link
        #print(f"Link set to {self.link}")
    
    def get_category(self):
        return self.category
    
    def set_category(self, value):
        self.category = value

    def get_driver(self):
        return self.driver
    
    def set_driver(self, value):
        self.driver = value

    def get_items(self):
        return self.items