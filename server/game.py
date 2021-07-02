import random, time
import ai
from threading import Thread

# This is the Game class, which holds most of the functions relating to
# the Tres game itself.

class Game():
    def __init__(self, id):
        # Card on top of the discard pile
        self.card = self.randomCard()

        # Stores the data of each player.
        # Each item has format [NAME, ID, [CARD1, CARD2, CARD3 ...]]
        # Or format [NAME, ID, [CARD1, CARD2, CARD3 ...], AI_FUNC (lawful, neutral, chaotic)]
        self.state = []

        # Index of player in self.state that has turn
        self.turn = 0

        # Which direction the turn advances
        self.direction = 1

    def players(self):
        # Gets list of player names
        players = []
        for player_data in self.state:
            players.append(player_data[0])
        return str(players)
    
    def numCards(self):
        # Gets the number of cards that each player has
        numCards = []
        for player_data in self.state:
            numCards.append([player_data[0], len(player_data[2])])
        return numCards

    def playerCards(self,player):
        # Gets the cards that one player has (ID required)
        for player_data in self.state:
            if player_data[1] == player:
                return player_data[2]
        return "error: player not found"

    def getPlayerData(self,player):
        # Gets player name and turn number.
        for i in range(len(self.state)):
            if self.state[i][1] == player:
                return {
                    "name":self.state[i][0],
                    "turn_number":i
                }
        return "error: player not found"

    def randomCard(self):
        # Generates a random card.
        color = random.choice(["R","B","G","P"]) # Red, Blue, Green, Purple
        symbol = random.choice(["0","1","2","3","4","5","6","7","8","9","PLUS","WILD","REVERSE","CANCEL"])
        return color+"_"+symbol

    def assignCards(self):
        # Randomly assigns seven cards to each player. Also clears existing cards.
        numCards = 7
        for player in self.state:
            player[2] = []
            for card in range(numCards):
                player[2].append(self.randomCard())

    def isMatching(self, card1, card2):
        # Tests if cards match in either color or symbol.

        color1, symbol1 = card1.split("_")
        color2, symbol2 = card2.split("_")

        if color1 == color2: return True
        if symbol1 == symbol2: return True

        if symbol2 == "WILD": return True

        return False

    def play(self, player, card, is_ai=False):
        # player (str): ID of player
        # card (str): card to play
        # is_ai (bool): if the player is an AI, bypass the ID checks  

        if is_ai:
            player_num = self.turn
        else:
            # First, find the player that matches with the ID
            for i in range(len(self.state)):
                if self.state[i][1] == player:
                    player_num = i
                    break
            else:
                return "error: player not found"

            # Check if it is the player's turn
            if player_num != self.turn:
                return "error: not player's turn"
        
        # Check if the player actually has the card
        if not(card in self.state[player_num][2]):
            # If it's a wild card, the color doesn't matter
            if card.split("_")[1] == "WILD":
                for c in self.state[player_num][2]:
                    if c.split("_")[1] == "WILD":
                        # Wild matches anything, we can skip the matching test
                        self.card = card
                        self.state[player_num][2].remove(c)
                        self.advanceTurn()
                        self.playAI()
                        return "success"
                else:
                    return "error: card not in player's hand"
            else:
                return "error: card not in player's hand"
        
        # Check if the card matches with the current top card
        if self.isMatching(self.card, card):
            # Make the move
            self.state[player_num][2].remove(card)
            self.card = card

            # Reverse card (acts like skip in two player game)
            if self.card.split("_")[1] == "REVERSE":
                if len(self.state) > 2:
                    self.direction *= -1
                else:
                    self.advanceTurn()

            # Skip card
            if self.card.split("_")[1] == "CANCEL":
                self.advanceTurn()

            # Give turn to next player
            self.advanceTurn()

            # +2 card
            if self.card.split("_")[1] == "PLUS":
                for i in range(2):
                    self.state[self.turn][2].append(self.randomCard())
        
            self.playAI()

            return "success"
        return "error: cards do not match"

    def draw(self, player):
        for i in range(len(self.state)):
            if self.state[i][1] == player:
                if i == self.turn:
                    self.state[i][2].append(self.randomCard())
                    self.advanceTurn()
                    self.playAI()
                    return "success"
                else:
                    return "error: not player's turn"
        return "error: player not found"

    def getData(self, player):
        # Sends the cards that player has, the number of cards
        # that each of the other players have, and whose turn it is.

        # player (str): ID of player

        return {
            "player_cards":self.playerCards(player),
            "num_cards":self.numCards(),
            "top_card":self.card,
            "turn":self.turn,
        }
    
    def advanceTurn(self):
        # Moves turn one player in self.direction
        self.turn = (self.turn + self.direction) % len(self.state)

    def playAI(self):
        # Check if it is an AI's turn; if so, calls runAI in a new thread
        print("Starting AI")
        if self.state[self.turn][1] == "BOT":
            # A thread must be used because the AI has a time-delay built in,
            # so otherwise the original player move would not return until
            # all the AIs finished their moves.
            t = Thread(target = self.runAI)
            t.start()
    
    def runAI(self):
        move = ai.lawful_AI(self.state[self.turn][2], self.card)
        if move == "draw":
            print("playAI: received draw command")
            self.state[self.turn][2].append(self.randomCard())
            self.advanceTurn()
            self.playAI()
        else:
            self.play("AI",move,True)