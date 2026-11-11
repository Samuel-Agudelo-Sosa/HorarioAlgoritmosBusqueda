#Se define clase abstracta (funcionará como una interfaz)
from abc import ABC, abstractmethod


class problema(ABC):

    def __init__(self, estado_inicial, operaciones, estado_meta):
        self.estado_inicial = estado_inicial
        self.operaciones = operaciones
        self.estado_meta = estado_meta


    @abstractmethod
    def operaciones(self, estado):
         #Retorna operaciones ejecutables desde el estado actual
        pass

    @abstractmethod
    def aplicar_operacion(self, estado, operacion):
        #Retorna el nuevo estado resultante de aplicar la acción al estado dado
        pass


    def costo_ruta(self, estado, operacion, estado_siguiente):
        return 1

    def es_meta(self, estado):
        return estado == self.estado_meta


    def heuristica(self, estado):
        #Se deja en 0 para los no informados.
        pass



