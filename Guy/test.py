from unittest import TestCase
from Guy import overig_functies as vf

class TestVelocity(TestCase):
    def test_velocity(self):
        self.assertEqual(27, vf.velocity())
