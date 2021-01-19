import unittest
import pandas as pd
import numpy as np
import readExternalData
from datetime import timedelta


class testTime(unittest.TestCase):
    def test_add_hour(self):
        timeDF = pd.DataFrame({"timestamp": ['01-01-2021 00:00:00',
                                             '01-01-2021 01:00:00',
                                             '01-01-2021 02:00:00',
                                             '01-01-2021 03:00:00'],
                               "Value": [1, 2, 3, 4]})

        newDF = pd.DataFrame({"timestamp": ['01-01-2021 01:00:00',
                                            '01-01-2021 02:00:00',
                                            '01-01-2021 03:00:00',
                                            '01-01-2021 04:00:00'],
                              "Value": [1, 2, 3, 4]})

        newDF.timestamp = pd.DatetimeIndex(newDF.timestamp) + timedelta(hours=0)

        pd.testing.assert_frame_equal(readExternalData.add_hour(timeDF), newDF)
