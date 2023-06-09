# -*- coding: utf-8 -*-
from PySide2.QtCore import QObject, Signal
from pathlib import Path

# absolut path of dir resicled
PATH_RESICLED = Path(__file__).resolve().parents[1]

class Tool():
    def __init__(self, parent=None):
        self.path_database_tables = self.get_path_database_tables()
        self.prefix_name_database = "resicled_" #"Database_resicled"
        
    def get_path_database_tables(self) -> str:
        return str(PATH_RESICLED.joinpath('databases','tables'))
    
    def get_path_database_tables_file(self, filename: str) -> str:
        return str(PATH_RESICLED.joinpath('databases','tables', filename))
    
