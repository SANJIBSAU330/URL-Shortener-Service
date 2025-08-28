from sqlmodel import SQLModel, Field
from pydantic import HttpUrl
from typing import Optional
from datetime import datetime


class ShortUrl(SQLModel,table=True):
    """schema for shortutl """
    short_url: str=Field(default = None, primary_key=True)
    original_url: str
    expire_at: Optional[datetime] = None
 

class GenerateUrl(SQLModel):
    """schema for take original url"""
    original_url: HttpUrl
    
class GenerateUrlUpdate(SQLModel):
    """schema for update url"""
    original_url: Optional[str] = None
