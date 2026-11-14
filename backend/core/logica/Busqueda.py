from abc import ABC, abstractmethod

class Busqueda(ABC):

    def __init__(self, control=3, maximo_nodos =50000):
        self.control = control
        self.maximo_nodos = maximo_nodos
        self.nodos_evaluados = 0

    def es_valido(self, hijo, nodo, explorados): 
    #control redundancia
        if self.control == 1 and nodo.padre and hijo == nodo.padre:
            #nodo.padre evita errores de padre nulo (cortocircuito)
            return False
        if self.control == 2:
            nodo_actual = nodo
            while nodo_actual:
                if nodo_actual == hijo:
                    return False
                nodo_actual = nodo_actual.padre
        if self.control == 3 and hijo.estado in explorados:
            #Filtro globalen tabla hash/set que es o(1) 
            return False


    def comprobar_limite(self):
        if self.nodos_evaluados > self.maximo_nodos:
            raise RuntimeError(
                f"Se superó el límite de seguridad ({self.maximo_nodos} nodos)."
            )

    
    @abstractmethod
    def busqueda(self, problema):
        pass