from fastapi import FastAPI
import sqlalchemy
from db import Base, engine
# Import schemas to test pydantic
from schemas import JobIn

app = FastAPI()

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    TABLES_CREATED = True
except Exception as e:
    TABLES_CREATED = str(e)

@app.get("/")
def read_root():
    return {
        "Hello": "World",
        "SA": sqlalchemy.__version__,
        "Tables": TABLES_CREATED,
        "SchemaTest": JobIn.model_json_schema()
    }

@app.get("/health")
def health():
    return {"status": "ok"}
