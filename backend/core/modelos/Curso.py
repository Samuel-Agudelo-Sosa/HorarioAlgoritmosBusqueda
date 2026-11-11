class Curso:

    def __init__(self, id_curso, nombre, duracion):
        self.id_curso = id_curso
        self.nombre = nombre
        self.duracion = duracion


    def __repr__(self):
        return f"Curso({self.id_curso}, {self.nombre}, {self.duracion}h)"