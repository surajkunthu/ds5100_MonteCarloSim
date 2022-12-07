'''
DS 5100 Final Project
Monte Carlo Simulation Tests
UVA MSDS
Suraj Kunthu
sk9km
'''

from montecarlo import Die, Game, Analyzer
import unittest
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal

class Test1_Die(unittest.TestCase):
    '''
    Class to test Die Class in montecarlo.py
    '''
    test1 = Die(faces=[1, 2, 3, 4, 5, 6])

    def test_1_change_weight(self):
        face = 6
        new_weight = 2
        Test1_Die.test1.change_weight(face = face, new_weight = new_weight)
        changed_face = np.where(Test1_Die.test1.faces == face)
        value_check = Test1_Die.test1.weight[changed_face] == new_weight
        self.assertTrue(value_check, "Weight was not changed.")
    
    def test_2_roll_die(self):
        run_rolls = Test1_Die.test1.roll_die(rolls = 4)
        value_check = str(type(run_rolls))
        self.assertEqual(value_check, "<class 'list'>", "Incorrect output type")

    def test_3_show_die(self):
        test_list_face = [1, 2, 3, 4, 5, 6]
        test_list_weight = [1.0, 1.0, 1.0, 1.0, 1.0, 2.0]
        value_check1 = Test1_Die.test1.die_df["Face"].tolist()
        value_check2 = Test1_Die.test1.die_df["Weight"].tolist()
        self.assertEqual(test_list_face, value_check1, "Die face does not match")
        self.assertEqual(test_list_weight, value_check2, "Die weight does not match")

class Test2_Game(unittest.TestCase):
    '''
    Class to test Game Class in montecarlo.py
    '''
    test2 = Die(faces = [1,2,3])
    test3 = Die(faces = [1,2,3,4,5,6])
    test4 = Die(faces = ["A" ,"B" ,"C"])

    def test_4_play(self):
        play_game = Game(object_list = [Test2_Game.test2, Test2_Game.test3])
        play_game.play(rolls = 6)
        value_check = play_game.results.shape
        self.assertEqual(value_check, (6,2), "Test results do not match expected shape (6,2)")

    def test_5_show(self):
        play_game = Game(object_list = [Test2_Game.test2, Test2_Game.test3, Test2_Game.test4])
        play_game.play(rolls = 6)
        value_check= play_game.show(form="narrow").shape
        self.assertEqual(value_check, (18,), "Narrow format does not work")

class Test3_Analyzer(unittest.TestCase):
    '''
    Class to test Analyzer Class in montecarlo.py
    '''
    test5 = Die(faces = [1])
    test6 = Die(faces = [2])

    def test_6_count_face(self):
        coin_test = Game(object_list = [Test3_Analyzer.test5, Test3_Analyzer.test6])
        num_rolls = 5
        coin_test.play(rolls = num_rolls)
        coin_test_score = Analyzer(coin_test)
        value_check = coin_test_score.count_face()
        data = [[1,1]] * num_rolls
        dummy_data = pd.DataFrame(data, columns=[1, 2], index=[*range(1, num_rolls+1, 1)])
        dummy_data.index.name = "Roll Number"
        assert_frame_equal(value_check, dummy_data)

    def test_7_jackpot(self):
        winner = Game(object_list = [Test3_Analyzer.test5, Test3_Analyzer.test5, Test3_Analyzer.test5])
        num_rolls = 5
        winner.play(rolls = num_rolls)
        jkpt_score = Analyzer(winner)
        test_score = jkpt_score.jackpot()
        value_check = num_rolls
        self.assertEqual(test_score, value_check, f"{value_check} were rolled, however, jackpot() method != {value_check}.")

    def test_8_combo(self):
        winner = Game(object_list = [Test3_Analyzer.test5, Test3_Analyzer.test5, Test3_Analyzer.test5])
        num_rolls = 7
        winner.play(rolls = num_rolls)
        combo_score = Analyzer(winner)
        combo_test = combo_score.combo()
        value_check = pd.DataFrame(data=[num_rolls], columns=["Combo Frequency"],index=["[1,1,1]"])
        assert_frame_equal(combo_test.reset_index(drop=True),value_check.reset_index(drop=True), "Combo table and Test table do not match")

if __name__ == '__main__':
    unittest.main(verbosity = 3)
