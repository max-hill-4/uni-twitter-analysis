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

if __name__ == '__main__':
    import time 
    start = time.time()
    selenium_test()
    end = time.time()
    print(f'Selenium took {end - start} seconds')
    start = time.time()
    playright_test()
    end = time.time()
    print(f'Playright took {end - start} seconds')
    start = time.time()
    scrapy_test()
    end = time.time()
    print(f'Scrapy took {end - start} seconds')


# Selenium took 13.267854452133179 seconds
# Playright took 4.521850109100342 seconds
# Scrapy took 1.4669597148895264 seconds