from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import RedirectResponse
from database import create_db, get_db
import random
import string
from sqlmodel import Session,select
from schemas import ShortUrl,GenerateUrl
from datetime import datetime,timedelta

app=FastAPI(title="URL Shortener Service")
@app.on_event("startup")
def create_db_table():
    create_db()

def generate_url(len=6):
    """ This function is generate a random string and length if the string is 6 which help to enerate url"""
    return  ''.join(random.choices(string.ascii_letters + string.digits, k=len))

@app.post("/short_url")
def create_short_url(data: GenerateUrl, session:Session = Depends(get_db)):
    """this function is use for short url.
    user can give original url """
    short = generate_url()
    while session.get(ShortUrl, short):
        short = generate_url()

    expire_time=(datetime.now()+timedelta(minutes=1))
    short_urls = ShortUrl(
        short_url=short,
        original_url=str(data.original_url),
        expire_at=expire_time
    )
    session.add(short_urls)
    session.commit()
    session.refresh(short_urls)

    return {
        "short_code": short_urls.short_url,
        "short_url": f"http://localhost:8000/{short_urls.short_url}",
        "expires_at": short_urls.expire_at
    }

@app.get("/show_all_URL")
def all_url(session:Session=Depends(get_db)):
    data1=session.exec(select(ShortUrl)).all()
    if not data1:
        raise HTTPException(status_code=400,detail="there is no URL")
    res=[]
    for data in data1:

        res.append({

            "short_url":f"http://localhost:8000/{data.short_url}",
            "expire":data.expire_at,
            "original_url":data.original_url,
            "short_code":data.short_url
        })
    return res
    


@app.delete("/Delete_URL/{short_code}")
def delete_url(short_code,session:Session=Depends(get_db)):
    data=session.get(ShortUrl,short_code)
    if not data:
        raise HTTPException(status_code=404,detail="url not found!")
    session.delete(data)
    session.commit()
    return data


@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.get(ShortUrl, short_code)

    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")

    if url_entry.expire_at < datetime.now():
        raise HTTPException(status_code=410, detail="URL expired")

    return RedirectResponse(url=url_entry.original_url)



    



