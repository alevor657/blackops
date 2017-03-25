"""
Weapon module
"""

from materials import Materials

class Weapon(Materials):
    """
    A weapon class
    """

    def __init__(self, material_type, price):
        self.classlvl = 3
        super().__init__(material_type, price, self.classlvl)
