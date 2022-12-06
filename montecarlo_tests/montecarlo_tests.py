from montecarlo.montecarlo import Die, Game, Analyzer
import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

class DieTestSuite(unittest.TestCase):

    def test_does_weight_change(self):
        a = Die(faces=[1,2,3,4])
        facevalue = 2
        newWeight = 3
        a.change_the_weight(facevalue=facevalue, newWeight=newWeight)
        faceindex = a.faces.index(facevalue)
        testValue = a.weights[faceindex] == newWeight
        error = "Your weight was not added to the face you specified."
        self.assertTrue(testValue, error)
    
    def test_roll_returns_list(self):
        b = Die(faces=[1,2,3,4,5,6])
        bigwinner = b.roll_die(times=4)
        testValue = str(type(bigwinner))
        expectedValue = "<class 'list'>"
        message = "Your output was not type list."
        self.assertEqual(testValue,expectedValue,message)

    def test_die_df_face(self):
        c = Die(faces=[1,2,3,4,5,6,7,8,9])
        facelist = c.faces
        testValue = c.die['face'].tolist()
        error = "Your die face column in the die df doesn't match the faces attribute."
        self.assertEqual(facelist,testValue,error)

    def test_die_df_weight(self):
        c = Die(faces=[1,2,3,4,5,6,7,8,9])
        weightslist = c.weights
        testValue = c.die['weight'].tolist()
        error = "Your die weights column in the die df doesn't match the weights attribute."
        self.assertEqual(weightslist,testValue,error)


class GameTestSuite(unittest.TestCase):

    def test_dataframe_play_size(self):
        a = Die(faces=[1,2,3,4])
        b = Die(faces=[1,2,3,4,5,6])
        craps = Game(dieList=[a,b])
        craps.play(times=4)
        testValue=craps.gameresults.shape
        expectedValue=(4,2)
        error = "Your play results' dataframe is not the expected shape."
        self.assertEqual(testValue,expectedValue,error)

    def test_narrow_dataframe_test(self):
        a = Die(faces=[1,2,3,4])
        b = Die(faces=[1,2,3,4,5,6])
        c = Die(faces=["a","b","c","d","e"])
        roller = Game(dieList=[a,b,c])
        roller.play(times=4)
        expectedValue=(12,)
        testValue= roller.show(format="narrow").shape
        error="Setting your dataframe to narrow didn't work."
        self.assertEqual(testValue,expectedValue,error)


class AnalyzerTestSuite(unittest.TestCase):

    def test_analyzer_face_frequency(self):
        a = Die(faces=[1])
        b = Die(faces=[2])
        realistic = Game(dieList=[a,b])
        realistic.play(times = 3)
        score = Analyzer(realistic)
        testValue = score.face_counts_per_roll()
        data = [[1,1],[1,1],[1,1]]
        df = pd.DataFrame(data, columns=[1,2], index=[1,2,3])
        df.index.name = "Roll Number"
        expectedValue = df
        assert_frame_equal(testValue,expectedValue)

    def test_analyzer_jackpot(self):
        a = Die(faces=[1])
        simple = Game(dieList=[a,a,a])
        simple.play(times=4)
        simplescore = Analyzer(simple)
        testValue = simplescore.jackpot()
        expectedValue = 4
        error = "You rolled 4 jackpots but your jackpot method did not return 4."
        self.assertEqual(testValue,expectedValue,error)

    def test_analyzer_combinations(self):
        a = Die(faces=[1])
        simple = Game(dieList=[a,a,a])
        simple.play(times=4)
        simplescore = Analyzer(simple)
        testValue = simplescore.combinations()
        expectedValue = pd.DataFrame(data=[4], columns=["Frequency of Combination"],index=["[1,1,1]"])
        error = "Your combinations table doesn't match the expected combinations table."
        assert_frame_equal(testValue.reset_index(drop=True),expectedValue.reset_index(drop=True))

if __name__ == '__main__':
    unittest.main(verbosity=3)
