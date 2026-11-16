from backend.logica.Nodo import Nodo
from backend.logica.Busqueda import Busqueda

class ProfundidadLimitada(Busqueda):
    def __init__(self, limite=10, control=3, maximo_nodos=50000):
        super().__init__(control=control, maximo_nodos = maximo_nodos)
        self.limite = limite

    def busqueda(self, problema):
        self.nodos_evaluados = 0
        nodo_actual = Nodo(problema.estado_inicial)

        frontera = [nodo_actual] #usamos lista como pila lifo normal
        explorados = {nodo_actual.estado} if self.control == 3 else set()
        hubo_poda = False # bandera que indiica si se podó una rama por límite

        while frontera:
            nodo_actual = frontera.pop()
            self.nodos_evaluados += 1
            self.comprobar_limite()

            if problema.es_meta(nodo_actual.estado):
                return nodo_actual

            if nodo_actual.profundidad < self.limite:
                for hijo in reversed(nodo_actual.generarHijos(problema)):
                    #reversed para que funcione como lifo y el primer hijo quede en el tope
                    if self.es_valido(hijo, nodo_actual, explorados):
                        if self.control == 3:
                            explorados.add(hijo.estado)
                        frontera.append(hijo)
            else:
                if problema.operaciones(nodo_actual.estado):
                    hubo_poda = True
        return "poda" if hubo_poda else None
        #poda si todavía había nodos por expandir y none si el espacio de búsqueda se agotó