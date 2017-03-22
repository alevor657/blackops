from employee import Employee

class Manager(Employee):
    def __init__(self, name, classlvl):
        self.occupation = "Manager"
        self.classlvl = 2
        super().__init__(name, self.occupation, self.classlvl)
