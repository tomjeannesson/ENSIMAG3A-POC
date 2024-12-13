import json

from fastapi import FastAPI
from board import Board

app = FastAPI()


# List of list


a = { "board" : [["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"],
    ["a","a","a","a","a","a","a","a"]
    ] }


pour_Julian = []
game_test = Board()
for i in range(8):
    for j in range(8):
        pour_Julian.append (game_test.board[0][0].name)
        



@app.get("/")
def read_root():
    return a

#Return un dictionnaire qui contient les données que je veux envoyer