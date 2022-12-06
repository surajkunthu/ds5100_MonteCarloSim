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
    Takes an array of faces as an argument.
    The array's data type (dtype) may be strings or numbers.
    The faces must be unique; no duplicates.
    Internally Initializes the weights to 1.0 for each face.
    Saves faces and weights in a private dataframe that is to be shared by the other methods.
    '''
    def __init__(self, faces):
        '''
        Create the Die
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

        find_weight = np.where(self.faces == face)
        self.weight[find_weight] = float(new_weight)
        self.die_df["Weight"] = self.weight
    

    def roll_die(self, rolls = 1):
        '''
        Method to roll the die, receive random die roll results
        '''
        # Use the random library and choice method to return a list with the randomly selected element from the specified sequence.
        result = random.choices(self.faces, weights = self.weight, k = rolls)
        return(result)

    def show_die(self):
        return(self.die_df)

# Game Class ---------------------------------------------
class Game:
    """
    A game consists of rolling one or more dice of the same kind, one or more times. This class can play a game or show the results of the most recent play.
    """
    def __init__(self, object_list):
        self.die_objects = object_list
    
    def play(self, times):
        '''Plays the game by rolling your list of dice as many times as you specify. Stores and returns the results.'''
        self.gameresults = pd.DataFrame()
        dicenumber = 1
        for m in self.die_objects:
            mResults = m.roll_die(times=times)
            name = f"Die Number {dicenumber}"
            mSeries = pd.Series(mResults, name=name)
            mDF = pd.DataFrame(mSeries)
            if dicenumber == 1:
                self.gameresults = mDF
            else:
                self.gameresults = self.gameresults.join(mDF)
            dicenumber += 1
        self.gameresults.index = self.gameresults.index + 1
        self.gameresults.index.name = "Roll Number"
        return(self.gameresults)

    def show(self, format="wide"):
        '''Shows the game results as a narrow or wide data frame - defaults to wide.'''
        try:
            if format == "wide":
                return(self.gameresults)
            elif format == "narrow":
                return(self.gameresults.stack())
        except ValueError as e:
            print("The variable 'format' must be either 'wide' or 'narrow.'.")
    
# Analyzer Class ---------------------------------------------
class Analyzer:
    '''
    An analyzer takes the results of a single game and computes various descriptive statistical properties about it.

    These properties are available as attributes of an Analyzer object.

    Attributes (and associated methods) include:

    A face counts per roll, i.e. the number of times a given face appeared in each roll. For example, if a roll of five dice has all sixes, then the counts for this roll would be 6 for the face value '6' and 0 for the other faces.
    A jackpot count, i.e. how many times a roll resulted in all faces being the same, e.g. six ones for a six-sided die.
    A combo count, i.e. how many combination types of faces were rolled and their counts.
    A permutation count, i.e. how may sequence types were rolled and their counts.
    '''
    
    def __init__(self, game):
        self.game = pd.DataFrame(game.show())

    def face_count(self):
        '''
        Returns and saves a frequence table for the roll results of your game, per roll.
        '''
        self.facefreq = (self.game.apply(pd.Series.value_counts, axis=1).fillna(0))
        return(self.facefreq)

    def jackpot(self):
        '''
        Stores a data frame of all jackpots (where every die rolled the same face) and which roll number they were. Returns only the number of jackpots.
        '''
        colnum = self.game.shape[1]
        self.face_count()
        hits = self.facefreq[self.facefreq.isin([colnum]).any(axis=1)]
        jacknum = hits.shape[0]
        self.jackpots = hits
        return(jacknum)

    def combo(self):
        '''
        Computes all combinations of faces taht were rolled in a game, saves and returns a frequency table for these combinations.
        '''
        colnum = self.game.shape[1]
        self.rollcombinations = self.game.apply(lambda x : sorted(list(x.iloc[0:colnum])), axis=1).value_counts().to_frame('Frequency of Combination')
        return(self.rollcombination)