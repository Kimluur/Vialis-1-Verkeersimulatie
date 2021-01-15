from unittest import TestCase
from Guy.wachtrij import tel
from Guy.Vialis_Functies import csv2pd
from Guy.wachtrij import wachtrij_achteraf

class TestWachtrij(TestCase):

    def test_wachtrij(self):
        """
        Check for wrong input, check how many times a sensor is activated (not how many 10th of a seconds its activated)
        """

        # self.assertEqual('2', tel(df['011']))

    def test_wachtrij_achteraf(self):
        """
        Checks for wrong input, checks if the cars are caculated correctly and if the data is correctly added to the dictionary
        """
        df = csv2pd('test.csv')
        rijbanen = [['01','011']]
        eind = wachtrij_achteraf(rijbanen, df)
        self.assertEqual(1, list(eind[rijbanen[0][2]].values())[0])
