from unittest import TestCase
from Guy.wachtrij import tel
from Guy.Vialis_Functies import csv2pd

class TestWachtrij(TestCase):
    def test_wachtrij(self):
        """
        Check for wrong input, check how many times a sensor is activated (not how many 10th of a seconds its activated)
        """
        df = csv2pd('test.csv')
        self.assertEqual('2', tel(df['011']))