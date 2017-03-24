"""
Moule for all workers
"""

from workers import Workers

class Employee(Workers):
    """
    A class for all workers
    """

    def __init__(self, name, occupation, classlvl, backpack=None):
        super().__init__(name, occupation, classlvl)
        self.backpack = backpack

    # def get_backpack(self):
    #     return self.backpack
    #
    # def add_to_backpack(self, item):
    #     self.backpack.append(item)
    #
    # def remove_from_bakcpack(self, item):
    #     self.backpack.remove(item)
