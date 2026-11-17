class VariableCurso:
    def __init__(self, id_variable, curso, profesores):
        self.id_variable = id_variable
        self.curso = curso
        self.profesores = profesores


    def __repr__(self):
        nombres = [p.nombre for p in self.profesores]
        return f"Variable({self.id_variable}: {self.curso.nombre} - Profs={nombres})"