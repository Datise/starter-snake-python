import json
import os
import random

import bottle
from bottle import HTTPResponse


@bottle.route("/")
def index():
    return "Your Battlesnake is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))

    response = {"color": "#b300ff", "headType": "bwc-snowman", "tailType": "bolt"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )

def check_board_collision(board, pos):
    
    disallowed = []
    print("X: " + str(pos["x"]))
    print("Y: " + str(pos["y"]))
    if pos["x"] - 1 < 0:
        disallowed.append("left")
    if pos["x"] + 1 > board["width"] - 1:
        disallowed.append("right")
    if pos["y"] - 1 < 0:
        disallowed.append("up")
    if pos["y"] + 1 > board["height"] - 1:
        disallowed.append("down")
    
    print(disallowed)
    return disallowed

def check_body_collision(pos):
    disallowed = []
    
def get_disallowed_moves(board, current_pos):
    disallowed = check_board_collision(board, current_pos[0])
    disallowed = disallowed + check_body_collision(current_pos)
    return disallowed

def decide_turn(board, body, turn):
    disallowed_moves = get_disallowed_moves(board, body)
    allowed_moves  =  []
    moves = ["down", "up", "left", "right"]
    for move in moves:
        if move not in disallowed_moves:
            allowed_moves.append(move)

    if turn % 2 == 0 and not (turn % 4 == 0) and "down" in allowed_moves:
        move = "down"
    elif turn % 3 == 0 and not (turn % 4 == 0) and "left" in allowed_moves:
        move = "left"
    elif turn % 4 == 0 and "up" in allowed_moves:
        move = "up"
    else:
        if "right" in allowed_moves:
            move = "right"
        else: 
            move = allowed_moves[0]

    if turn == 0 and "up" not in disallowed_moves:
        move = "up"
    
    if turn == 1 and "right" not in disallowed_moves:
        move = "right"

    return move

@bottle.post("/move")
def move():
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    data = bottle.request.json
    print("MOVE:", json.dumps(data))

    # Choose a random direction to move in
    # directions = ["up", "down", "left", "right"]
    # move = random.choice(directions)    
    move = decide_turn(data["board"], data["you"]["body"], data["turn"])    
    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "I am a python snake!"

    response = {"move": move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    print("END:", json.dumps(data))
    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()
