from backend.logica.Nodo import Nodo
from backend.logica.Busqueda import Busqueda

from backend.core.algoritmos.ProfundidadLimitada import ProfundidadLimitada

class ProfundidadIterativa(Busqueda):
    def __init__(self, limite_maximo=float('inf'), control=3, maximo_nodos=500000):
        super().__init__(control=control, maximo_nodos = maximo_nodos)
        self.limite_maximo = limite_maximo

    def busqueda(self, problema):
        self.nodos_evaluados = 0
        profundidad = 0

        while profundidad <= self.limite_maximo:
            profundidad_limitada = ProfundidadLimitada(limite=profundidad, control= self.control, maximo_nodos=self.maximo_nodos)
            resultado = profundidad_limitada.busqueda(problema)

            self.nodos_evaluados += profundidad_limitada.nodos_evaluados
            self.comprobar_limite()

            if isinstance(resultado, Nodo):
                return resultado

            if resultado is None:
                return None
            #si se obtuvo poda en el otro algo, se incrementa la profundidad para la siguiente iteracion

            profundidad +=1

        return None


