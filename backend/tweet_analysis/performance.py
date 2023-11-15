# Test for different scraping methods

# Selenium

def selenium_test():
    # Need to test different browsers
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    driver = webdriver.Firefox()
    get_1 = driver.get('https://example.com')
    driver.quit()

# Playright 

def playright_test():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://example.com")
        browser.close()

# Scrapy

def scrapy_test():
    import scrapy
    from scrapy.crawler import CrawlerProcess
    class TestSpider(scrapy.Spider):
        name = 'test'
        start_urls = ['https://example.com']
    process = CrawlerProcess()
    process.crawl(TestSpider)
    process.start()
