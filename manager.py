from employee import Employee

class Manager(Employee):
    def __init__(self, name, classlvl, backpack=None):
        self.occupation = "Manager"
        self.classlvl = 2
        self.backpack = backpack
        super().__init__(name, self.occupation, self.classlvl, self.backpack)
