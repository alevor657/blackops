from workers import Workers

class Employee(Workers):
    def __init__(self, name, occupation, classlvl, backpack=[]):
        self.name = name
        self.occupation = occupation
        self.classlvl = classlvl
        self.backpack = backpack

    def get_backpack(self):
        return self.backpack

    def add_to_backpack(self, item):
        self.backpack.append(item)

    def remove_from_bakcpack(self, item):
        self.backpack.remove(item)
