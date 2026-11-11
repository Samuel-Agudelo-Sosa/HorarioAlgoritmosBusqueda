# estructuras/Cola.py

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class Cola:
    """Cola FIFO implementada mediante lista enlazada con nodos."""
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamaño = 0

    def encolar(self, elemento):
        nuevo_nodo = Nodo(elemento)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.tamaño += 1

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("Desencolar de una cola vacía")
        dato = self.cabeza.dato
        self.cabeza = self.cabeza.siguiente
        if self.cabeza is None:
            self.cola = None
        self.tamaño -= 1
        return dato

    def esta_vacia(self):
        return self.tamaño == 0

    def __len__(self):
        return self.tamaño