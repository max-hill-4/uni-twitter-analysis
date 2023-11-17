# Webscraping for tweets
# Data cleaning

import asyncio
from pyppeteer import launch

async def get_tweet(tweet):
    browser = await launch(
    handleSIGINT=False,
    handleSIGTERM=False,
    handleSIGHUP=False
    )
    page = await browser.newPage()
    await page.goto(tweet)

    xpath = ('//*[contains(@data-testid, "tweetTex")]')

    await page.waitForXPath(xpath)
    element = await page.xpath(xpath)

    text_content = await page.evaluate('(element) => element.textContent', element[0])

    await browser.close()
    return text_content



