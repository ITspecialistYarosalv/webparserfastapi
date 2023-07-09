from sqlalchemy import (Column,Integer,MetaData,String,Table)
from database import engine
metadata = MetaData()
Article = Table(
    "article",
    metadata,
    Column("id",Integer,primary_key = True),
    Column("title",String(100)),
    Column("author", String(100)),
    Column("time", String(100)),
    Column("link", String(100)),
    Column("category",String(1000),default="Article")
)

metadata.create_all(engine)