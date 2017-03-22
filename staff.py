from employee import Employee

class Staff(Employee):
    def __init__(self, name, classlvl):
        self.occupation = "Staff"
        self.classlvl = 1
        super().__init__(name, self.occupation, self.classlvl)
