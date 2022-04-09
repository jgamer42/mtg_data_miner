from urllib import response
import requests
from lxml import html ,etree
import asyncio
from pyppeteer import launch

def get_card_price(card_name:str):
    response = requests.get("https://www.tcgplayer.com/search/magic/product?productLineName=magic&productName=nissa&view=grid")
    #response = requests.get("https://www.tcgplayer.com/search/magic/product?productLineName=magic&productName=Usher%20of%20the%20Fallen&view=grid")
    raw_page = html.fromstring(response.text)
    a = raw_page.xpath("//div[@class='centered']/div[@class='pagination__arrow']/following-sibling::div/button/span/text()")
    print(a)
    
    b = open("salida.html","w+")
    b.write(response.text)
    b.close()


async def aux ():
    browser = await launch()
    page = await browser.newPage()
    await page.goto("https://www.tcgplayer.com/search/magic/product?productLineName=magic&productName=Usher%20of%20the%20Fallen&view=grid")
    #await page.screenshot({"path":"salida.png"})
    a = page.waitForXPath("//div[@class='centered']/div[@class='pagination__arrow']/following-sibling::div/button/span/text()")
    primt(a)
asyncio.get_event_loop().run_until_complete(aux())