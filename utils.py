import asyncio
import aiohttp
from starlette.responses import StreamingResponse

from models import  Article
from bs4 import BeautifulSoup as bs
from config import URLS
from sqlalchemy import select
from fastapi import APIRouter,HTTPException,status,Response
from schemas import ArticleSchema,ArticleSchemaIn
from database import database,get_csv_data
rounter = APIRouter(tags=['Articles'])


async def pars(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            return html

async def save_article(article_title, author, publication_date, link, category):
    query = select([Article]).where(
        (Article.c.title == article_title) &
        (Article.c.author == author) &
        (Article.c.time == publication_date) &
        (Article.c.link == link) &
        (Article.c.category == category)
    )
    existing_article = await database.fetch_one(query)

    if existing_article is None:
        insert_query = Article.insert().values(
            title=article_title,
            author=author,
            time=publication_date,
            link=link,
            category=category
        )
        await database.execute(insert_query)
    else:
        print("All is done")

async def bbs():
    html = await pars(URLS[0])
    soup = bs(html, 'html.parser')

    articles = soup.find_all('article')

    for article in articles:
        title_element = article.find('h3', class_='lx-stream-post__header-title')
        article_title = title_element.get_text(strip=True)
        author_element = article.find('p', class_='qa-contributor-name')
        try:
            author = author_element.get_text(strip=True)
        except:
            author = "Not find"
        link_element = article.find('a')
        link = link_element['href']
        time_element = article.find('time', class_='lx-stream-post__meta-time')
        time = time_element.find('span', class_='qa-post-auto-meta').get_text()
        category = "Article"

        await save_article(article_title, author, time, link, category)



@rounter.get('/articles/')
async def get_articles():
    query = Article.select()
    return await database.fetch_all(query)

@rounter.get('/articles/{id}', response_model=ArticleSchemaIn)
async def get_details(id: int):
    query = Article.select().where(id == Article.c.id)
    myarticle = await database.fetch_one(query)

    if not myarticle:
        return HTTPException
    return {**myarticle}

@rounter.delete('/articles/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def del_article(id: int):
    query = Article.delete().where(Article.c.id == id)
    await database.execute(query)
    return {"message": "It's all done"}

@rounter.get('/download')
async def download_file(response: Response):
    csv_data = get_csv_data()

    # Встановлення заголовків відповіді для скачування файлу
    headers = {
        "Content-Disposition": "attachment; filename=data.csv",
        "Content-Type": "text/csv",
    }

    return StreamingResponse(iter([csv_data]), headers=headers)

@rounter.get('/parse')
async def parse_and_save_data():
    await database.connect()
    asyncio.gather(bbs())