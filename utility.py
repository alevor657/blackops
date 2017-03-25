"""
Utility module
"""

from materials import Materials

class Utility(Materials):
    """
    A Utility class
    """

    def __init__(self, material_type, price):
        self.classlvl = 1
        super().__init__(material_type, price, self.classlvl)
