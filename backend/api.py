import json

import numpy as np
from board import Board
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://poc-thaj:8000/",
    "http://poc-thaj:3000/",
    "http://poc-thaj:8000",
    "http://poc-thaj:3000",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

board = Board()


@app.get("/")
def read_root():
    with open("data.json") as f:
        data = json.load(f)
        if len(data) == 64:
            board.update(data)
            with open("logs.txt") as l:
                print("update", file=l)

        else:
            with open("logs.txt") as l:
                print(len(data), data, file=l)
    boardJson = []
    for i in range(8):
        row = []
        for j in range(8):
            if board.board[i][j] == {}:
                row.append(None)
            else:
                row.append(board.board[i][j].name)
        boardJson.append(row)
    return boardJson
