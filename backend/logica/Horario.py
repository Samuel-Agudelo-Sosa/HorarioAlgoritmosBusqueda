from backend.logica.Problema import Problema

class Horario(Problema):
    #inicializar el problema de asignación de horarios.
    
    def __init__(self, variables_curso, franjas, salones):
        #siendo un problema de satisfación de restricciones
        #no tiene meta con estado fijo, sino una condición a cumplir 
        #por eso el estado meta se pasa en none
        super().__init__(estado_inicial=(), estado_meta=None)
        self.variables_curso = variables_curso
        self.franjas = franjas
        self.salones = salones

        #Diccionarios de acceso O(1) para buscar objetos por ID
        self.mapa_variables = {v.id_variable: v for v in variables_curso}
        self.mapa_franjas = {f.id_franja: f for f in franjas}
        self.mapa_salones = {s.id_salon : s for s in salones}


    def es_meta(self, estado):
        #Restricción Dura: Cada clase debe asignarse exactamente una vez
        return len(estado) == len(self.variables_curso)
        #Es meta cuando la cantidad de asignaciones es igual a la cantidad de clases


    def operaciones(self, estado):

        if self.es_meta(estado): #no buscar más cursos de los disponibles 
            return [] #para evitar overflow abajo con variables_curso[len(estado)]
        #se toma la siguiente clase a asignar
        #evita que un curso se evalué dos veces o quede sin evaluar
        siguiente_var = self.variables_curso[len(estado)]
        operaciones_validas = []

        for franja in self.franjas:
            if franja.duracion() < siguiente_var.curso.duracion:
                continue
            for salon in self.salones:
                if self.cumple_restricciones_duras(estado, franja, salon, siguiente_var.profesor):
                    operacion = (siguiente_var.id_variable, franja.id_franja, salon.id_salon)
                    operaciones_validas.append(operacion)

        return operaciones_validas

    def cumple_restricciones_duras(self, estado, franja_nueva, salon_nuevo, profesor_nuevo):
        #verificar cruce de la nueva franja y salón contra todas las clases ya asignadas
        for id_var_asig, id_franja_asig, id_salon_asig in estado:
            franja_asig = self.mapa_franjas[id_franja_asig]
            var_asig = self.mapa_variables[id_var_asig]

            # si las franjas se cruzan
            # Al ser el horario para un único semestre (un solo grupo), 
            # NINGUNA clase puede solaparse en el tiempo con otra clase del mismo semestre.
            if franja_nueva.se_cruza_con(franja_asig):
                # Restricción Dura 1: Un salón no puede tener dos clases en la misma franja horaria
                # if salon_nuevo.id_salon == id_salon_asig:
                #     return False
                
                # Restricción Dura 2: Un profesor no puede dictar dos clases en la misma franja horaria
                # if profesor_nuevo.id_profesor == var_asig.profesor.id_profesor:
                #     return False
                return False
            
        return True

    def aplicar_operacion(self, estado, operacion):
        #se usa concatenación de tuplas para inmutabilidad y hash en sets
        return estado + (operacion,) 

    def costo_ruta(self, estado, operacion, estado_siguiente):
        return 1 #costo de asignación es 1

    def heuristica(self, estado):
        #Heurística base para A*: cantidad de clases que faltan por asignar
        #Es admisible porque asume un costo mínimo de 1 por cada clase restante
        return len(self.variables_curso) - len(estado)
    


