class Material:
    def __init__(self,name:str, type:str,demrecycling:float, demenergy:float, demwaste:float,brorec:float, broener:float, browaste: float,price : float):
        self.name : str = name
        self.type : str = type
        self.demrec : float = demrecycling
        self.demener: float = demenergy
        self.demwaste: float = demwaste
        self.brorec: float = brorec
        self.broener: float = broener
        self.browaste: float = browaste
        self.price: float = price
        self.polluant : bool = name in ['PWB','LCD','Cable (high current)','Cable (low current)', 'Battery (Lead-acid)','Battery (Ni-Cd)','Other battery','CPT','Cable (optical)','Bulb','Cartouche encre'] or name[:3]=='PWB'       

    def setPolluant(self,status: bool)-> None:
        self.polluant=status

    def __str__(self) -> str:
        return "Material : \n Name : {} \n Type : {} \n Demrec : {} \n Demener : {} \n Demwaste : {}\n Brorec : {} \n Broener : {} \n browaste : {}\n".format(self.name,self.type,self.demrec,self.demener,self.demwaste,self.brorec,self.broener,self.browaste)
