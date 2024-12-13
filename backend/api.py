import json

from fastapi import FastAPI

from board import Board

app = FastAPI()
board = Board()


@app.get("/")
def read_root():
    boardJson = []
    # with open("state.json") as f:
    #     board_state = json.load(f)
    # board.move()
    for i in range(8):
        row = []
        for j in range(8):
            row.append(board.board[i][j].name)
        boardJson.append(row)
    return {"board": boardJson}
