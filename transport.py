"""
Transport module
"""

from materials import Materials

class Transport(Materials):
    """
    A Transport class
    """

    def __init__(self, material_type, price):
        self.classlvl = 2
        super().__init__(material_type, price, self.classlvl)
