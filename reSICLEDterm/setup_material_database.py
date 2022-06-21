import os
from brightway2 import *
import json
from bw2io.package import BW2Package

def setupDict(filename):
    # takes the json file, returns the dict that will be written in the database
    with open(filename, "r") as f:
        jdata=json.load(f)
    newData={}
    for material in jdata:
        newMat = {}
        newMat["Name"]=material["material name"]
        newMat["Type"]=material["material type"]
        newMat["Dismantling recovery"]=material["after dismantling"]["recovery potential"]
        newMat["Dismantling energy"]=material["after dismantling"]["energy recovery potential"]
        newMat["Dismantling waste"]=material["after dismantling"]["residual waste potential"]
        newMat["Shredding recovery"]=material["after shredding"]["recovery potential"]
        newMat["Shredding energy"]=material["after shredding"]["energy recovery potential"]
        newMat["Shredding waste"]=material["after shredding"]["residual waste potential"]
        newMat["Pollutant"] = material["material name"] in ['PWB','LCD','Cable (high current)','Cable (low current)', 'Battery (Lead-acid)','Battery (Ni-Cd)','Other battery','CPT','Cable (optical)','Bulb','Cartouche encre'] or material["material name"][:3]=='PWB'
        newData[("Materials",newMat["Name"])]=newMat
    return newData

if __name__=="__main__":
    projects.set_current("reSICLED")
    db = Database("Materials")
    db.write(setupDict("data.json"))
    BW2Package().export_obj(db,filename="Materials",folder=os.getcwd())    

