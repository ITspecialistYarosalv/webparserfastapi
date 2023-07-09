from config import URLS
import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs

async def pars(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            return html

async def foreginaffeirs():
    html = await pars(URLS[1])
    soup = bs(html, 'html.parser')
    articles = soup.find_all('div')
    for article in articles:
        print(article)
        h2_element = article.find('h3', class_="title ls-0 mb-0 mt-2")
        try:
            atag = h2_element.find('a', class_="ob-l")
            article_title = atag.get_text()
            link = atag['href']

            author_element = article.find('div', class_='author fst-italic f-serif ob ls-0')
            author = author_element.get_text(strip=True)

            category_element = article.find('span', class_='category text-uppercase')
            category = category_element.get_text(strip=True)

            date_element = article.find('span', class_='publication-date text-uppercase')
            publication_date = date_element.get_text(strip=True)
        except:
            article_title = "None"
            link = "None"
            author = "None"
            category = "None"
            publication_date ="None"

async def main():
    await foreginaffeirs()

asyncio.run(main())