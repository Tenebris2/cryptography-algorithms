import fastapi
from algorithms.rsa import *

app = fastapi.FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "world"}
