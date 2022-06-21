from .material import Material

class Piece:
    def __init__(self,name : str, weight : float, material_type : str, material : Material, amount : int):
        self.name=name
        self.weight=weight
        self.material_type=material_type
        self.material=material
        self.amount=amount

    def __str__(self):
        return "Piece : \n\n Name : {} \n Weight : {} \n Material Type : {} \n Material : {} \n Amount : {} \n".format(self.name,self.weight, self.material_type, self.material, self.amount)