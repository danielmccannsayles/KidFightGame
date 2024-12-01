## Kid Fight Game
Have an imaginary fight.. but real!

### Setup instructions:

1. Create a new venv, and activate it
2. Pip install -r requirements.txt
4. all the game stuff is in game_stuff

### Background
#### Main game
llm folder contains llm calling.  
testing contains mocks and testing stuff for the game.  
client contains clientside UI renderingk, pygame, and network (allows for clientside communication w/ server).  
server contains all game logic & handlers, clocks, methods, etc.  

#### Old stuff

##### Game_v1
Contains the game before its logic & UI were split up and it was turned into multiplayer

##### Network Game
tclient and tserver are testing for the network
Network stuff - stuff involved w/ the network

