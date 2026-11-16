from collections import deque
from backend.logica.Nodo import Nodo
from backend.logica.Busqueda import Busqueda

class Amplitud(Busqueda):

    def busqueda(self, problema):
        self.nodos_evaluados = 0
        nodo_actual = Nodo(problema.estado_inicial)

        frontera = deque([nodo_actual]) #cola FIFO
        explorados = {nodo_actual.estado} if self.control == 3 else set()

        while frontera:
            nodo_actual = frontera.popleft() #saca el primer elemento
            self.nodos_evaluados += 1
            self.comprobar_limite() #no supere máximo de nodos definidos

            #inicio de proceso de expansión
            if problema.es_meta(nodo_actual.estado):
                return nodo_actual

            for hijo in nodo_actual.generarHijos(problema):
                if self.es_valido(hijo, nodo_actual, explorados): #control de redundancia
                    if self.control == 3:
                        explorados.add(hijo.estado)
                    frontera.append(hijo)
        return None



