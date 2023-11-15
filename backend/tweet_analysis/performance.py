# Test for different scraping methods

def selenium_test():
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    driver = webdriver.Firefox()
    get_1 = driver.get('https://example.com')
