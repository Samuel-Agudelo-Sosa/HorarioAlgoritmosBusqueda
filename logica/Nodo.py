from collections import deque

class Nodo:

    def __init__(self, estado, padre=None, operacion=None, g=0):
        self.estado = estado
        self.padre = padre
        self.operacion = operacion #ayuda a obtener el camino de la solucion
        self.g = g
        self.profundidad = 0 if self.padre is None else self.padre + 1


    def generarHijos(self, problema):
        hijos = []
        for operacion in problema.operaciones(self.estado):
            nuevo_estado = problema.aplicar_operacion(self.estado, operacion)
            nuevo_nodo = Nodo(estado = nuevo_estado, padre = self, 
                operacion = operacion,
                g = self.g + problema.costo_ruta(self.estado, operacion, nuevo_estado))
            hijos.append(nuevo_nodo)
        return hijos


    def camino_nodos(self):
        #retorna la lista de nodos desde la raíz hasta el nodo actual
        nodo_actual = self
        camino = deque()
        while nodo_actual:
            camino.appendleft(nodo_actual) #agrega al inicio convirtiendo la estructura en LIFO
            nodo_actual = nodo_actual.padre

        return list(camino)



    def camino_solucion(self):
        return [nodo.operacion for nodo in self.camino_nodos() if nodo.operacion is not None]
        #No hay operacion (none) para llegar a la raíz por eso la validación