class Profesor():
    def  __init__(self, id_profesor,  nombre, id_cursos, franjas_no_disponibles=None):
        self.id_profesor = id_profesor
        self.nombre = nombre
        self.id_cursos = id_cursos
        self.franjas_no_disponibles = set(franjas_no_disponibles) if franjas_no_disponibles else set()



    def __repr__(self):
        return f"Profesor({self.id_profesor}, {self.nombre}, Cursos={self.id_cursos})"