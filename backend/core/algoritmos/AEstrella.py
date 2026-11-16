from backend.core.algoritmos.BusquedaPrimeroMejor import BusquedaPrimeroMejor

class AEstrella(BusquedaPrimeroMejor):
    def __init__(self, control=3, maximo_nodos = 50000):
        super().__init__(f=lambda nodo, problema: problema.heuristica(nodo.estado) + nodo.g, control=control, maximo_nodos=maximo_nodos)
