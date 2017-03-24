"""
Employee module
"""

from employee import Employee

class Staff(Employee):
    """
    A class for low level personal
    """

    def __init__(self, name, classlvl, backpack):
        self.occupation = "Staff"
        self.classlvl = 1
        self.backpack = backpack
        super().__init__(name, self.occupation, self.classlvl, self.backpack)
