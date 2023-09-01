"""
 Creat a Player class to represent the Player entity properly.
"""
import unittest
class Player:
    def __init__(self, name, clothes):
        """
             Constructor method
        :param name: Player's name
        :param clothes: Player's clothes
        :return None
        """
        self.name = name
        self.clothes = clothes
        self.backpack = []
        self.health = 'poisoned'
        self.smell = 'smells'


    def dressUp(self, clothes):
        self.clothes.append(clothes)

    def takeItem(self, item):
        self.backpack.append(item)

class TestPlayer(unittest.TestCase):
    """
         Define an unit test for Player class
    :param: unittest.TestCase
    :return: None
    """
    def setUp(self):
        """Runs prior to each unit test """
        self.p1 = Player
    def tearDown(self):
        """Runs after each unit test """
        self.p1.contents.clear()
    def test_1(self):
        self.assertTrue(self.p1.takeItem('pen'))
        self.assertTrue(self.p1.dressUp('coat'))
