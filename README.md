# Tres
*By Jieruei Chang 2021*

![Tres picture](https://user-images.githubusercontent.com/30610197/124502398-6803ad80-dd91-11eb-8c46-1585ae59c987.png)

TRES is an online Uno clone. It features multiplayer support, a clean UI, and somewhat competent AI players with different strategies. It uses a HTML/JS frontend hosted on Github Pages,
and a Flask backend running on PythonAnywhere. You can play at [knosmos.github.io/tres](https://knosmos.github.io/tres).

## Gameplay
The objective is to be the first player to play all of the cards in their hand. At the start of the game, each player is dealt seven cards.
On their turn, a player may play one card from their hand, or draw a card from the deck. A played card must have the same number/symbol or
color as the card currently at the top of the discard pile. If they cannot play any cards, they must draw. The implemented "Special cards"
(Reverse, Cancel, +2, Wild) function identically to regular Uno.

## Running TRES locally
### Dependencies
- flask
- flask-cors

### Folder structure
The Flask server code is stored in the `server` directory. The client code is stored in the `docs` directory. The `docs` directory is named that way
because Github Pages annoyingly only supports serving from root or `docs`. All image assets are stored in `docs/assets`.

### Starting the server
Navigate to the `server` directory and run `py server.py`.

### Connecting to the server
Take note of the web address that the server displays. It should look something like `http://192.168.1.4:5000/`.
Open `docs/constants.js` and change the value of `SERVERURL` (which should be `https://tres3.pythonanywhere.com`) with the server address. Open `index.html` and
you should be able to play.
