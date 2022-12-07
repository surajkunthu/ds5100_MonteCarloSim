'''
DS 5100 Final Project
Monte Carlo Simulation
UVA MSDS
Suraj Kunthu
sk9km
'''
import numpy as np
import pandas as pd
import random

# Die Class ---------------------------------------------
class Die:
    '''
    A die has N sides, or “faces”, and W weights, and can be rolled to select a face.
     - Takes an array of faces as an argument.
     - The array's data type (dtype) may be strings or numbers.
     - The faces must be unique; no duplicates.
     - Internally Initializes the weights to 1.0 for each face.
     - Saves faces and weights in a private dataframe that is to be shared by the other methods.
    '''
    def __init__(self, faces):
        '''
        Create the Die
        Faces can be a list of ints, floats, or strings
        '''
        self.faces = np.unique(np.array(faces))
        self.weight = np.ones(len(faces))
        self.die_df = pd.DataFrame({"Face": self.faces, "Weight": self.weight})

    def change_weight(self, face, new_weight):
        '''
        A method to change the weight of a single side.
        '''
        # Checks to see if the face passed is valid; is it in the array of weights?
        if face not in self.faces:
            print("Face is not valid, not in the array of weights")
            return
        # Checks to see if the weight is valid; is it a float? Can it be converted to one?
        if not isinstance(new_weight, (float, int)):
            print("Invalid data type")
            return
        # Create an identifer to search in dataframe
        find_weight = np.where(self.faces == face)
        # replace value in with new value
        self.weight[find_weight] = float(new_weight)
        # place new value in dataframe
        self.die_df["Weight"] = self.weight

    def roll_die(self, rolls = 1):
        '''
        Method to roll the die, receive random die roll results
        '''
        # Use the random library and choice method to return a list with the randomly selected element from the specified sequence.
        result = random.choices(self.faces, weights = self.weight, k = rolls)
        return(result)

    def show_die(self):
        '''
        A method to show the user the die’s current set of faces and weights 
        '''
        return(self.die_df)

# Game Class ---------------------------------------------
class Game:
    """
    A game consists of rolling of one or more dice of the same kind one or more times.
    The class has a behavior to play a game, i.e. to roll all of the dice a given number of times.
    """
    def __init__(self, object_list):
        '''
        Initialize Game by passing Die object to Game
        '''
        self.die_objects = object_list
    
    def play(self, rolls):
        '''
        Play method takes a parameter to specify how many times the dice should be rolled.
        Stores and returns the results.
        '''
        # Intialize a results DF
        self.results = pd.DataFrame()
        # start iter at 1
        m_die = 1
        # check EACH die roll in Die objects list
        for n_roll in self.die_objects:
            # Store Die roll method results
            dice_results = n_roll.roll_die(rolls = rolls)
            # Store values as a series type
            dice_results_series = pd.Series(dice_results, name = f"Die Number {m_die}")
            # Put series into a data frame
            dice_results_df = pd.DataFrame(dice_results_series)
            # Store results df as results
            if m_die == 1:
                self.results = dice_results_df
            else:
                self.results = self.results.join(dice_results_df)
            # Go to next die
            m_die = m_die + 1
        # increase the index by 1
        self.results.index = self.results.index + 1
        # roll number as a named index
        self.results.index.name = "Roll Number"
        return(self.results)

    def show(self, form = "Wide"):
        '''
        Show method displays th user the results of the most recent play in narrow or wide (default) dataframe.
        '''
        try:
            if (form == "Narrow" or form == "narrow"):
                return(self.results.stack())
            elif (form == "Wide" or form == "wide"):
                return(self.results)
        # Raise exception on invalid data format
        except ValueError as e:
            print("Invalid Data Format. Must be 'narrow' or 'wide'.")
    
# Analyzer Class ---------------------------------------------
class Analyzer:
    '''
    An analyzer takes the results of a single game and computes various descriptive statistical properties about it.

    These properties are available as attributes of an Analyzer object.

    Attributes (and associated methods) include:
     - A face counts per roll, i.e. the number of times a given face appeared in each roll. For example, if a roll of five dice has all sixes, then the counts for this roll would be 6 for the face value '6' and 0 for the other faces.
     - A jackpot count, i.e. how many times a roll resulted in all faces being the same, e.g. six ones for a six-sided die.
     - A combo count, i.e. how many combination types of faces were rolled and their counts.
     - A permutation count, i.e. how may sequence types were rolled and their counts.
    '''
    
    def __init__(self, game_object):
        '''
        Initialize Analyzer Class, takes a game object as its input parameter.
        '''
        self.game_object = pd.DataFrame(game_object.show())

    def count_face(self):
        '''
        Method to compute how many times a given face is rolled in each event.
        '''
        # The dataframe with index as the roll number and face values as columns (i.e. it is in wide format).
        self.roll_count = (self.game_object.apply(pd.Series.value_counts, axis=1).fillna(0))
        return(self.roll_count)

    def jackpot(self):
        '''
        Method to compute how many times the game resulted in all faces being identical.
        '''
        # Retrieve number of columns
        num_col = self.game_object.shape[1]
        # Run the count_face method to find matches
        self.count_face()
        # Look for matches in dataframe along columns, sum up counts
        num_identical = self.roll_count[self.roll_count.isin([num_col]).any(axis=1)]
        # Find the numb
        winners = num_identical.shape[0]
        # store number of winners in jackpots
        self.jackpot_winners = num_identical
        return(winners)

    def combo(self):
        '''
        Method to compute the distinct combinations of faces rolled, along with their counts.
        '''
        # Retrieve number of columns
        num_col = self.game_object.shape[1]
        # Apply lambda function to get number of distinct combinations of faces rolled
        self.combos = self.game_object.apply(lambda combo: sorted(list(combo.iloc[0:num_col])), axis=1).value_counts().to_frame("Combo Frequency")
        return(self.combos)