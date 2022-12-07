# Monte Carlo Simulator
DS5100 Final Project Fall 2022 \
Suraj Kunthu \
sk9km \
UVA School of Data Science

## Synopsis
----
## Installing

Clone the git repo:
```bash
git clone https://github.com/surajkunthu/ds5100_MonteCarloSim.git
```

Next install the package:
```bash
!pip install montecarlo
```

## Importing

Import into your python code
```python
from ds5100_MonteCarloSim.montecarlo.montecarlo import Die, Game, Analyzer
```

There are three classes: `Die`, `Game`, and `Analyzer`

## Creating dice objects
```python
test = Die(faces = [])
```
## Playing games

```python
test_game = Game(object_list = [test])
test_game.play(rolls = )
```
## Analyzing games
```python
test_analyze = Game(game_object = [test_game])
test_analyze.jackpot()
test_analyze.combo()
```

## API description
## `Die` Class
Doc String: A die has N sides, or “faces”, and W weights, and can be rolled to select a face

Methods:
- `change_weights(self, face, weight)`: A method to change the weight of a single side
  - `self`.`face`: face chosen to change weight
  - `self`.`new_weight`: weight being changed
- `roll_die(self, rolls = 1)`: Method to roll the die, receive random die roll results
  - `self`.`rolls`: how many dice rolls?
- `show_die(self)`: A method to show the user the die’s current set of faces and weights 

## `Game` Class
Doc String: A game consists of rolling of one or more dice of the same kind one or more times. The class has a behavior to play a game, i.e. to roll all of the dice a given number of times

Methods:
- `play(self, rolls)`: Play method takes a parameter to specify how many times the dice should be rolled
  - `self`.`rolls`: how many rolls in game play
- `show(self, form = "Wide")`: method displays th user the results of the most recent play in narrow or wide (default) dataframe
  - `self`.`form`: choose "wide" (default) table or "narrow" table

## `Analyzer` Class
Doc String: An analyzer takes the results of a single game and computes various descriptive statistical properties about it
Methods:
- `count_face(self)`: Method to compute how many times a given face is rolled in each event
- `jackpot(self)`: Method to compute how many times the game resulted in all faces being identical
- `combo(self)`: Method to compute the distinct combinations of faces rolled, along with their counts