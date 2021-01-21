import unittest
from Main_Program.main import *


class testworld(unittest.TestCase):
    # creeer een vergelijkbare test wereld net als in de echte file.
    resolution = (1376, 984)
    win = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    pygame.display.set_caption("AutoSim")
    background = pygame.image.load('bg.png')
    autoBreedte = 40
    lusSizeDefault = (8, 8)

    # Json/ data related imports_
    dfKruis1 = loadJsontoDf("bos210.json")

    def test_binnen_scherm(self):
        """
        Test of de code met gegeven coordinaten binnen het scherm print.
        En dus ook of ze goed geprojecteerd worden.
        """
        test1 = latlngToScreenXY(51.6832962, 5.2938813)[0]
        self.assertEqual(test1 > 0 and test1 < 1377, True)
        test2 = latlngToScreenXY(30.6832962, 53.2938813)[0]
        self.assertEqual(test2 < 0 or test2 > 1377, True)

