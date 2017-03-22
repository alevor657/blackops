from employee import Employee

class Staff(Employee):
    def __init__(self, name, classlvl, backpack):
        self.occupation = "Staff"
        self.classlvl = 1
        self.backpack = backpack
        super().__init__(name, self.occupation, self.classlvl, self.backpack)
