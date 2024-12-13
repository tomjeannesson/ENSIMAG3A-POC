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

boardJson = []
with open("data.json") as f:
    board_state = json.load(f)
state_board_prev = board_state
array_prev = np.array(list(state_board_prev))


@app.get("/")
def read_root():
    with open("data.json") as f:
        board_state = json.load(f)
    state_board = board_state
    array_now = np.array(list(state_board))
    if state_board != state_board_prev:
        bit_pos_start = np.where(array_prev != array_now)[0]
        state_board_prev = state_board
        array_prev = array_now
        with open("data.json") as f:
            board_state = json.load(f)
        state_board = board_state
        while state_board == state_board_prev:
            with open("data.json") as f:
                board_state = json.load(f)
            state_board = board_state
        array_now = np.array(list(state_board))
        bit_pos_end = np.where(array_prev != array_now)[0]
        board.move(bit_pos_start, bit_pos_end)
    state_board_prev = state_board
    for i in range(8):
        row = []
        for j in range(8):
            if board.board[i][j] == {}:
                row.append(None)
            else:
                row.append(board.board[i][j].name)
        boardJson.append(row)
    return {"board": boardJson}
