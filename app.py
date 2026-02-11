from fastapi import FastAPI
import sqlalchemy

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World", "SA": sqlalchemy.__version__}

@app.get("/health")
def health():
    return {"status": "ok"}
