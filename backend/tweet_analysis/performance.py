# Test for different scraping methods

# Selenium

async def pyppeteer_test(website):
    import asyncio
    from pyppeteer import launch
    browser = await launch()
    page = await browser.newPage()
    await page.goto(tweet)
    xpath = ('//*[contains(@data-testid, "tweetTex")]')
    await page.waitForXPath(xpath)
    element = await page.xpath(xpath)
    text_content = await page.evaluate('(element) => element.textContent', element[0])
    await browser.close()
    return text_content

def selenium_test(website):
    # Need to test different browsers
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    get_1 = driver.get(website)
    driver.quit()

# Playright 

def playright_test(website):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(website)
        browser.close()

# Scrapy

def scrapy_test(website):
    import scrapy
    from scrapy.crawler import CrawlerProcess
    class TestSpider(scrapy.Spider):
        name = 'test'
        start_urls = [website]
    process = CrawlerProcess()
    process.crawl(TestSpider)
    process.start()

if __name__ == '__main__':
    import time 
    test_methods = [pyppeteer_test,selenium_test, playright_test, scrapy_test]
    results = []
    for method in test_methods:
        start = time.time()
        method('https://twitter.com/taylorswift13')
        end = time.time()
        results.append([method.__name__,end - start])
        
    print(results)

# Selenium took 13.267854452133179 seconds
# Playright took 4.521850109100342 seconds
# Scrapy took 1.4669597148895264 seconds