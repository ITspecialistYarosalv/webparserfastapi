from pydantic import BaseModel
from typing import Optional
class ArticleSchema(BaseModel):
    title:str
    link:str

class ArticleSchemaIn(ArticleSchema):
    id:int
