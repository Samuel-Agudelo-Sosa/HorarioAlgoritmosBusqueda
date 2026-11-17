import heapq # minheap
from backend.logica.Nodo import Nodo
from backend.logica.Busqueda import Busqueda

class BusquedaPrimeroMejor(Busqueda):
 
    def __init__(self, f, control=3, maximo_nodos = 500000):
        super().__init__(control=control, maximo_nodos=maximo_nodos)
        self.f = f

    def busqueda(self, problema):
        self.nodos_evaluados = 0
        nodo_actual = Nodo(problema.estado_inicial)

        orden_llegada = 0 #permite hacer un desempate por amplitud (orden de llegada FIFO)
        frontera = [] # Se va volver la cola de prioridad
        heapq.heappush(frontera, (self.f(nodo_actual, problema), orden_llegada, nodo_actual)) 
        #en el heappush primero ordena por función de costo
        #después si hay empate tiene prioridad el que llegó primero
        explorados = set()
        while frontera:
            #costo,ordenllegada,nodo
            _, _, nodo_actual = heapq.heappop(frontera)
            #heappop nos devuelve el primero en prioridad

            if self.control == 3 and nodo_actual.estado in explorados:
                #el nodo ya fue evaluado con menor costo por tanto se omite
                continue

            self.nodos_evaluados += 1
            self.comprobar_limite()


            if problema.es_meta(nodo_actual.estado):
                return nodo_actual

            if self.control == 3:
                explorados.add(nodo_actual.estado)

            for hijo in nodo_actual.generarHijos(problema):
                if self.es_valido(hijo, nodo_actual, explorados):
                    orden_llegada += 1
                    heapq.heappush(frontera, (self.f(hijo, problema), orden_llegada, hijo))

        return None



