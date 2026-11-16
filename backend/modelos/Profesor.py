class Profesor():
    def  __init__(self, id_profesor,  nombre, id_cursos):
        self.id_profesor = id_profesor
        self.nombre = nombre
        self.id_cursos = id_cursos


    def __repr__(self):
        return f"Profesor({self.id_profesor}, {self.nombre}, Cursos={self.id_cursos})"