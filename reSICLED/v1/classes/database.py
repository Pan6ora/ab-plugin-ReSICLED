import brightway2 as bw

class ProductDatabase:
    def __init__(self, name):
        # Creates the database in bw
        self.database = bw.Database(name)
        self.name = name

    def add(self, piece):
        # on suppose que la piece est bien concue pour la bdd
        dico = self.database.load()
        dico[(self.name,piece["Name"])]=piece
        self.database.write(dico)

    def get(self, key):
        # gets the piece by its name
        return self.database.get(key)
    
