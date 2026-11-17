
from backend.core.algoritmos.BusquedaPrimeroMejor import BusquedaPrimeroMejor
from backend.logica.Nodo import Nodo
from backend.logica.Busqueda import Busqueda

class CostoUniforme(BusquedaPrimeroMejor):
    def __init__(self, control=3, maximo_nodos = 500000):
        super().__init__(f=lambda nodo, problema: nodo.g, control=control, maximo_nodos=maximo_nodos)
