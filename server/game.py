class Game():
    def __init__(self, id):
        self.state = []
        self.turn = 0

    def players(self):
        players = []
        for player_data in self.state:
            players.append(player_data[0])
        return str(players)
        
    def checkMove(self, player, card):
        # First, check if the player actually has the card

        # Then, check if the card matches with the current top card
        pass