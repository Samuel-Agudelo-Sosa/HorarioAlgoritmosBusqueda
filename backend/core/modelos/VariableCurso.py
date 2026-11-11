class VariableCurso:
    def __init__(self, id_variable, curso, profesor):
        self.id_variable = id_variable
        self.curso = curso
        self.profesor = profesor


    def __repr__(self):
        return f"Variable({self.id_variable}: {self.curso.nombre} - Prof:{self.profesor.nombre})"