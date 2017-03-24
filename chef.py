"""
Module for Chef class
"""

from employee import Employee

class Chef(Employee):
    """
    A class for employees with highest acess level
    """
    def __init__(self, name, classlvl, backpack=None):
        self.occupation = "Chef"
        self.classlvl = 3
        self.backpack = backpack
        super().__init__(name, self.occupation, self.classlvl, self.backpack)
