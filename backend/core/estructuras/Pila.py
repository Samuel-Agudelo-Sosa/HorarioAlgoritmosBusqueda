class Pila:
    """Estructura LIFO (Last In, First Out) para el algoritmo DFS."""
    
    def __init__(self):
        self.elementos = []

    def apilar(self, item):
        self.elementos.append(item)

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("Desapilar de una pila vacía")
        return self.elementos.pop()

    def esta_vacia(self):
        return len(self.elementos) == 0

    def __len__(self): #le dice al método nativo como tener el tamaño de la pila
        return len(self.elementos)