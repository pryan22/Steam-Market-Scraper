
from driver import Driver as d
from sql import sql as s

if __name__ == "__main__":
    driver = d('chrome', "any")
    driver.crawl_pages("chroma")
    items = driver.get_items()
    sql = s()
    sql.add_items(items)
    sql.stop()
    driver.driver.close()
