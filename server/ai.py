'''
Uno2 AI opponents. There are three types of simple AI:
lawful, neutral and chaotic. Each has a distinct "personality"
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
    time.sleep(0.5)
    valid_cards = getAllValidMoves(cards, top_card)
    if len(valid_cards) == 0:
        print("lawful_AI: Drawing card")
        return "draw"
    for card in valid_cards:
        if card.split("_")[1].isdigit(): # Number card? Return that.
            print("lawful_AI: playing",card)
            return card
    print("lawful_AI: playing",valid_cards[0])
    return valid_cards[0] # Fine, return a special card

def neutral_AI(cards, top_card):
    # If it has a wild, it will immediately play it
    # and choose the color that it has the
    # most of. Otherwise, it will play a card from
    # the most common color in its hand.

    print("neutral_AI: thinking...")
    time.sleep(0.5)
    valid_cards = getAllValidMoves(cards, top_card)
    if len(valid_cards) == 0:
        print("neutral_AI: Drawing card")
        return "draw"
    card_colors = {
        "B":[],
        "G":[],
        "R":[],
        "P":[]
    }
    has_wild = False
    for card in cards:
        color, symbol = card.split("_")
        card_colors[color].append(symbol)
        if symbol == "WILD":
            has_wild = True
    chosen_color = max(card_colors, key=lambda i:len(card_colors[i])) # Choose color that is most common
    if has_wild:
        # If it has wild card, play it
        card = chosen_color+"_WILD"
    else:
        for c in valid_cards:
            if c.split("_")[0] == chosen_color:
                card = c
        else:
            card = valid_cards[0]
    print("neutral_AI: Playing",card)
    return card

def chaotic_AI(cards, top_card):
    # Essentially the opposite of lawful_AI. Plays all the special cards it can.
    time.sleep(0.5)
    valid_cards = getAllValidMoves(cards, top_card)
    if len(valid_cards) == 0:
        print("chaotic_AI: Drawing card")
        return "draw"
    for card in valid_cards:
        if not(card.split("_")[1].isdigit()): # Special card? Return that.
            print("chaotic_AI: playing",card)
            return card
    print("chaotic_AI: playing",valid_cards[0])
    return valid_cards[0] # Fine, return a number card