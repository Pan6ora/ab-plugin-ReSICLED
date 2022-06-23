import os
import brightway2 as bw

class MaterialDatabase:
    def __init__(self):
        if "Materials" not in bw.databases:
            # we need to import the database from the existing database
            pass

        