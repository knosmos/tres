'''
Uno2 AI opponents. There are three types of simple AI:
lawful, neutral and chaotic. Each has a distinct "philosophy"
to make the game more interesting.
'''

import time

def getAllValidMoves(cards, top_card):
    color1, symbol1 = top_card.split("_")
    res = []
    for card in cards:
        color2, symbol2 = card.split("_")
        if color1 == color2 or symbol1 == symbol2 or symbol2 == "WILD":
            res.append(card)
    return res

def lawful_AI(cards, top_card):
    # Plays nice. Hates special cards and only plays them
    # when it has no choice.
    print("AI: thinking...")
    time.sleep(1)
    valid_cards = getAllValidMoves(cards, top_card)
    if len(valid_cards) == 0:
        print("AI: Drawing card")
        return "draw"
    for card in valid_cards:
        if card.split("_")[1].isdigit(): # Number card? Return that.
            print("AI: playing",card)
            return card
    print("AI: playing",valid_cards[0])
    return valid_cards[0] # Fine, return a special card

def neutral_AI(cards, top_card):
    # If it has a wild, it will immediately play it
    # and choose the color that it has the
    # most of. Otherwise, it will play the card that
    # has the most common number or most common color
    # in its hand.
    pass

def chaotic_AI():
    # Plays a wild (random color), +2, swap or cancel
    # if one can be played. Otherwise,
    # chooses a random valid move.
    pass