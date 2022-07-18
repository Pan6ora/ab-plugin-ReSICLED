
from .materialdatabase import Materialdatabase
from .productdatabase import Productdatabase
from .composedatabase import Composedatabase
from .componentdatabase import Componentdatabase
from .directivedatabase import Directivedatabase

class DatabaseManager():
    def __init__(self, parent=None):
        #super(DatabaseManager, self).__init__(parent)
        self.materialdatabase = Materialdatabase()
        self.productdatabase = Productdatabase()
        self.composedatabase = Composedatabase()
        self.componentdatabase = Componentdatabase()
        self.directivedatabase = Directivedatabase()
