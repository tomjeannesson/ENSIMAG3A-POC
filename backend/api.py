import json

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    with open("state.json") as f:
        data = json.load(f)
    return data
