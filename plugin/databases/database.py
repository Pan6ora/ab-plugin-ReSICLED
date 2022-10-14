
from .materialdatabase import Materialdatabase
from .productdatabase import Productdatabase
from .composedatabase import Composedatabase
from .componentdatabase import Componentdatabase
from .directivedatabase import Directivedatabase
from .guidelinesdatabase import GuidelinesDatabase

class DatabaseManager():
    def __init__(self, parent=None):
        self.directivedatabase = Directivedatabase()
        self.productdatabase = Productdatabase()
        self.composedatabase = Composedatabase()
        self.componentdatabase = Componentdatabase()
        
        self.guidelinesdatabase = GuidelinesDatabase()
        self.materialdatabase = Materialdatabase()
