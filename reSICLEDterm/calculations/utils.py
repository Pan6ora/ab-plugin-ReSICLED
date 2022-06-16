from math import floor

def arrondi(nombre,precision):
    # precision = nombre de decimales ; nobmre = float
    p = nombre*(10**precision)
    if p%1<0.5:
        return float(floor(p))/(10**precision)
    else:
        return (float(floor(p)+1))/(10**precision)