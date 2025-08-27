from sqlmodel import SQLModel,Field
from pydantic import HttpUrl
from typing import Optional
from datetime import datetime


class ShortUrl(SQLModel,table=True):
    short_url:str=Field(default=None,primary_key=True)
    original_url:str
    expire_at:Optional[datetime]=None

class GenerateUrlm(SQLModel):
    expire_at:Optional[datetime]=None

class GenerateUrl(GenerateUrlm):
    original_url:HttpUrl
    