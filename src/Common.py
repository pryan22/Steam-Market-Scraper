import sys
from selenium.webdriver.remote.webelement import WebElement
import re
import Common as c

def error(type: str, message: str):
    if type == "moderate":
        print(f"There was a moderate error: {message}\n")
    if type == "critical":
        print(f"There was a critial error: {message}\n")
        print("Exiting...\n")
        sys.exit(2)
    else:
        print(f"Error: {message}")
        sys.exit(2)

#Formats the prices correctly
def fix_prices(prices:list[WebElement]):
    list = []
    for i in range(0, len(prices), 2):
        price = extract_price(prices[i].text)
        list.append(price)
    return list

#Extracts the price from the unformatted price
def extract_price(unformatted_price: str) -> str:
    dollar_sign_index = 0
    try:
        dollar_sign_index = unformatted_price.rfind('$')
    except:
        error("moderate", "Could not find price for an item")
    return unformatted_price[dollar_sign_index + 1:]

#Extracts the wear from the name
def extract_wear(name:str) -> str:
    match = re.search(r'\(([^)]*)\)', name)
    if match:
        return match.group(1)
    return None

#Extracts the skin from the name
def extract_skin(name:str) -> str:
    match = re.search(r'\| ([^(]+) \(', name)
    if match:
        return match.group(1)
    return None

#Extracts the item type from the name
def extract_item_type(name:str) -> str:
    match = re.search(r'(?:StatTrak™|Souvenir) (\w+)|(\w+)', name)
    if match:
        item = match.group(1) or match.group(2)
        return item
    return None

#Extracts if the item is stattrack
def extract_stattrack(name:str):
    if "StatTrak" in name:
        return True
    return False

#Extracts if the item is souvenir
def extract_souvenir(name:str):
    if "Souvenir" in name:
        return True
    return False
