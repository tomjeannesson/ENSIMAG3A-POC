import json
from fastapi import FastAPI
from board import Board

app = FastAPI()

@app.get("/")
def read_root():
    game_test = Board()
    boardJson = []
    for i in range(8):
        row = []
        for j in range(8):
            row.append(game_test.board[i][j].name)
        boardJson.append(row)
    return { "board": boardJson }