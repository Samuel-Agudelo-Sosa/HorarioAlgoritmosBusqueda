from backend.core.algoritmos.BusquedaPrimeroMejor import BusquedaPrimeroMejor

class AEstrella(BusquedaPrimeroMejor):
    def __init__(self, control=3, maximo_nodos = 500000):
        super().__init__(f=lambda nodo, problema: (
            problema.heuristica(nodo.estado) + nodo.g,
            problema.heuristica(nodo.estado)
            ), 
            control=control, 
            maximo_nodos=maximo_nodos)
