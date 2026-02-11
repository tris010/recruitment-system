from fastapi import FastAPI, Depends
import sqlalchemy
from sqlalchemy.orm import Session
from db import Base, engine, get_db

app = FastAPI()

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    TABLES_CREATED = True
except Exception as e:
    TABLES_CREATED = str(e)

@app.get("/")
def read_root():
    return {"Hello": "World", "SA": sqlalchemy.__version__, "Tables": TABLES_CREATED}

@app.get("/health")
def health():
    return {"status": "ok"}
