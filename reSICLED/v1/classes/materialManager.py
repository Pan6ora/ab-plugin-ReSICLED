#idee definition gestion materiaux
import brightway2 as bw

class MaterialsManager:
    def __init__(self,projectName="Resicled",databaseName="Materials"):
        bw.projects.set_current(projectName)
        self.database= bw.Database(databaseName)
        self.databaseName=databaseName

    def addNewMaterial(self,material):
        assert(type(material)==dict)
        assert(sorted(list(material.keys()))==sorted(["Name","Type","Polluant","Dismantling recovery","Dismantling energy","Dismantling waste","Shredding recovery","Shredding energy","Shredding waste"]))
        dico = self.database.load()
        dico[(self.databaseName,material["Name"])]=material
        self.databate.write(dico)

    
