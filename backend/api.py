import json

import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from board import Board

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
