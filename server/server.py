'''
Description: TRES is an online Uno clone. It features multiplayer support,
a clean UI, and AI players with different strategies.

This holds all of the server code that is used to
communicate with the clients.

Author: Jieruei Chang
Language: Python 3.9.5
Date: 7/5/2021
'''

''' INITIALIZATION '''

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import random
from game import Game
import ai

app = Flask(__name__)
CORS(app, support_credentials=True)

# Sets of all player and game IDs in use
used_player_ids = set()
used_game_ids = set()

# Games that are currently in waiting room
waiting_games = {}
# Games that are currently playing a game
running_games = {}

# Length of game and player IDs
id_length = 6

@app.route("/")
def index():
    return '''
    <h1>TRES</h1>
    <h2><i>all systems nominal</i></h2>
    <h2>Client webpage: <a href=https://knosmos.github.io/tres>knosmos.github.io/tres</a></h2>
    '''

''' GAME CREATION AND JOINING '''

def generateID(l,prev):
    # Generates a random string of length l
    # that is not in prev
    res = ""
    while not(res) and not(res in prev):
        res = ''.join(random.choice("0123456789") for _ in range(l))
    return res

@app.route("/create",methods=["POST"])
# ADD A PLAYER TO A NEW GAME
def createGame():
    # Get player name
    player_name = request.get_json(force=True)["name"]

    # Generate random IDs
    game_id = generateID(id_length, used_game_ids) # Generate an ID not used by any game
    player_id = generateID(id_length, used_player_ids)
    
    used_game_ids.add(game_id)
    used_player_ids.add(player_id)

    # Initialize game object
    game = Game(game_id)
    game.state.append([player_name,player_id,[]])
    waiting_games[game_id] = game
    print("Created game [",game_id,"], player id [",player_id,"], player name [",player_name,"]")
    return jsonify({"id":player_id, "game":game_id})

@app.route("/join",methods=["POST"])
# ADD A PLAYER TO AN EXISTING GAME
def joinGame():
    # Get player name and game ID
    json = request.get_json(force=True)
    player_name = json["name"]
    game_id = json["game"]

    # Generate random ID
    player_id = generateID(id_length, used_player_ids)
    used_player_ids.add(player_id)

    # Add player to game object
    if game_id in waiting_games:
        # Check that player name is unique
        if player_name in [waiting_games[game_id].state[i][0] for i in range(len(waiting_games[game_id].state))]:
            return "error: player name already in use"
        waiting_games[game_id].state.append([player_name,player_id,[]])
    else:
        return "error: nonexistent game"
    print("Add player [",player_name,"], id [",player_id,"], to game [",game_id,"]")
    return jsonify({"id":player_id, "game":game_id})

''' WAITING ROOM '''

@app.route("/lobby",methods=["GET","POST"])
# GET CURRENTLY CONNECTED PLAYERS, AND WHETHER GAME HAS STARTED.
def lobby():
    # Get game ID
    game_id = request.args["game"]
    try:
        player_id = request.args["id"]
    except:
        print("warning: player id not supplied in call to /lobby")
        player_id = False

    # Get player info
    if game_id in waiting_games: # If the game hasn't started yet, it will be in waiting_games.
        # Determine if player has been kicked
        kicked = "no"
        if player_id:
            if not (player_id in [waiting_games[game_id].state[i][1] for i in range(len(waiting_games[game_id].state))]):
                kicked = "yes"
        # Return data
        return jsonify({
            "players":waiting_games[game_id].players(),
            "start":"no",
            "kicked":kicked
        })
    elif game_id in running_games: # If the game has started, it will be in running_games.
        return jsonify({
            "players":running_games[game_id].players(),
            "start":"yes",
            "kicked":"no"
        })
    else:
        return "error: nonexistent game"

@app.route("/addAI",methods=["POST"])
# ADD AN AI TO THE GAME.
def addAI():
    # Get game ID
    json = request.get_json(force=True)
    game_id = json["game"]

    # Check if game is valid
    if game_id in waiting_games:
        # Find how many bots there are in the game;
        # this is used to get the bot name and to make sure there aren't
        # more than ten bots        
        names = ["Uno","Dos","Tres","Cuatro","Cinco","Seis","Siete","Ocho","Nueve","Diez"]
        num_bots = 0
        for player in waiting_games[game_id].state:
            if player[1] == "BOT":
                num_bots += 1
        if num_bots < 10:
            # Add BOT player to game object
            ai_type = random.choice([ai.lawful_AI, ai.neutral_AI, ai.chaotic_AI])
            # waiting_games[game_id].state.append([names[num_bots]+"Bot - "+ai_type.__name__,"BOT",[],ai_type])
            waiting_games[game_id].state.append([names[num_bots]+"Bot","BOT",[],ai_type])
        else:
            return "error: too many bots"
    else:
        return "error: nonexistent game"
    return "success"

@app.route("/remove",methods=["POST"])
# Kick a player from the game
def kick():
    json = request.get_json(force=True)
    game_id = json["game"]
    player_num = json["num"] # number of the player to kick
    player_id = json["id"]

    g = waiting_games[game_id].state

    if game_id in waiting_games:
        if g[0][1] == player_id:
            if g[player_num][1] != player_id:
                removed_player_name = g[player_num][0]
                g.pop(player_num)
                return "Successfully removed player "+removed_player_name
            return "You cannot remove yourself"
        return "Non-host players cannot remove players"
    return "error: nonexistent game"

''' GAME '''

@app.route("/start",methods=["POST"])
# START THE GAME
def startGame():
    # Get game ID
    json = request.get_json(force=True)
    game_id = json["game"]

    # Check if game is valid
    if game_id in waiting_games:
        # Move game from waiting_games to running_games
        running_games[game_id] = waiting_games[game_id]
        waiting_games.pop(game_id)
        # Initialize game state
        running_games[game_id].initialize()
        return "success"
    
    # Errors (not displayed to client, but useful for debugging)
    elif game_id in running_games:
        return "error: game already running"
    return "error: nonexistent game"

@app.route("/player_data",methods=["GET"])
# SEND PLAYER NAME AND TURN NUMBER
def getPlayerData():
    game_id = request.args["game"]
    player_id = request.args["id"]
    if game_id in running_games:
        return jsonify(running_games[game_id].getPlayerData(player_id))
    return "error: game not found"

@app.route("/data",methods=["GET"])
# SEND ALL GAME DATA TO PLAYERS
def getData():
    # Get game and player ID
    game_id = request.args["game"]
    player_id = request.args["id"]
    if game_id in running_games:
        return jsonify(running_games[game_id].getData(player_id))
    return "error: game not found"

@app.route("/play",methods=["POST"])
def playCard():
    json = request.get_json(force=True)

    game_id = json["game"]
    player_id = json["id"]
    card = json["card"]

    if game_id in running_games:
        running_games[game_id].play(player_id, card)
    return "error: game not found"

@app.route("/draw",methods=["POST"])
# ADD ONE CARD TO PLAYER'S HAND, ADVANCE TURN
def drawCard():
    json = request.get_json(force=True)
    game_id = json["game"]
    player_id = json["id"]
    if game_id in running_games:
        running_games[game_id].draw(player_id)
    return "error: game not found"

@app.route("/return",methods=["POST"])
# RETURN TO LOBBY ONCE GAME ENDS
def returnToLobby():
    json = request.get_json(force=True)
    game_id = json["game"]
    if game_id in running_games:
        waiting_games[game_id] = running_games[game_id]
        running_games.pop(game_id)
    return "error: game not found"

''' BOILERPLATE '''
if __name__ == "__main__":
    app.run('0.0.0.0')