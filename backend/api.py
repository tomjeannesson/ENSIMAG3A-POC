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
with open("data.json") as f:
    json.dump("0000000000000011111111111111111111111111111111110000000000000000", f)


@app.get("/")
def read_root():
    with open("data.json") as f:
        data = json.load(f)
        if len(data) == 64:
            board.update(data)
            print(board.board_to_bits(), data, board.board_to_bits() == data)

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
