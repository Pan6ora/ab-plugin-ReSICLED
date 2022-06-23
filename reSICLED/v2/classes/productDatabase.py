import brightway2 as bw

class ProductDatabase:
    def __init__(self, productName):
        self.database = bw.Database(productName)
        self.productName = productName

    def addPiece(self,piece):
        # assertion : piece is in the right data format
        dico = self.database.load()
        dico[(self.productName,piece["Name"])]=piece
        self.database.write(dico)

