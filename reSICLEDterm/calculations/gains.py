from classes.piece import Piece
from .utils import arrondi

def gain1(piece : Piece, arrond : int)-> float:
    if not piece.material.polluant:
        return arrondi(piece.material.demrec - piece.material.brorec, arrond)
    else:
        return 0.

def gain2(piece : Piece, arrond : int) -> float:
    if piece.material.polluant:
        return 0.
    else:
        return arrondi(piece.material.demrec+piece.material.demener-piece.material.brorec-piece.material.broener,arrond)

def relativeWeight(piece : Piece, piecesList : list, arrond : int) -> float:
    """
    Returns the relative weight of the piece among the whole unit
    """
    return arrondi(piece.weight/sum([piece.weight for piece in piecesList]), arrond)

def weight(piecesList : list) -> float:
    return sum([piece.weight for piece in piecesList])