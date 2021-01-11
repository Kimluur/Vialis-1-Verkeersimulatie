from unittest import TestCase
from Guy import Vialis_Functies as vf


class TestVelocity(TestCase):
    def test_velocity(self):
        self.assertIn("|", vf.velocity())
