import json

from fastapi import FastAPI

app = FastAPI()


# Je recupere une liste de liste

a = { "board" : [["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"]
    ] }

@app.get("/")
def read_root():
    return a

#Return un dictionnaire qui contient les données que je veux envoyer