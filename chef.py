from employee import Employee

class Chef(Employee):
    def __init__(self, name, classlvl):
        self.occupation = "Chef"
        self.classlvl = 3
        super().__init__(name, self.occupation, self.classlvl)
