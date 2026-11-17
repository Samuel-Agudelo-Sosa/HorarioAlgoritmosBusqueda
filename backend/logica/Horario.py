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
        self.mapa_profesores = {
            p.id_profesor: p
            for v in variables_curso
            for p in v.profesores

        }


    def es_meta(self, estado):
        #Restricción Dura: Cada clase debe asignarse exactamente una vez
        return len(estado) == len(self.variables_curso)
        #Es meta cuando la cantidad de asignaciones es igual a la cantidad de clases


    def operaciones(self, estado):

        if self.es_meta(estado): #no buscar más cursos de los disponibles 
            return [] #para evitar overflow abajo con variables_curso[len(estado)]
        #se toma la siguiente clase a asignar
        #evita que un curso se evalué dos veces o quede sin evaluar
        var_actual = self.variables_curso[len(estado)]
        operaciones_validas = []

        for prof in var_actual.profesores:
            for franja in self.franjas:
                if franja.duracion() < var_actual.curso.duracion:
                    continue
                salon = self.salones[len(estado) % len(self.salones)] #round roubin
                if self.cumple_restricciones_duras(estado, prof, franja, salon):
                    operacion = (var_actual.id_variable, prof.id_profesor, franja.id_franja, salon.id_salon)
                    operaciones_validas.append(operacion)

        return operaciones_validas

    def cumple_restricciones_duras(self, estado, prof_nuevo, franja_nueva, salon_nuevo):
        #verificar cruce de la nueva franja y salón contra todas las clases ya asignadas
        for id_var_asig, id_prof_asig, id_franja_asig, id_salon_asig in estado:
            franja_asig = self.mapa_franjas[id_franja_asig]
            var_asig = self.mapa_variables[id_var_asig]

            # si las franjas se cruzan
            # Al ser el horario para un único semestre (un solo grupo), 
            # NINGUNA clase puede solaparse en el tiempo con otra clase del mismo semestre.
            if franja_nueva.se_cruza_con(franja_asig):
  
                return False
            
        return True

    def aplicar_operacion(self, estado, operacion):
        #se usa concatenación de tuplas para inmutabilidad y hash en sets
        return estado + (operacion,) 

    def costo_ruta(self, estado, operacion, estado_siguiente):
        costo = 1
        id_var, id_profesor, id_franja, id_salon = operacion
        var = self.mapa_variables[id_var]
        prof = self.mapa_profesores[id_profesor]
        franja_nueva =self.mapa_franjas[id_franja]
        #Restricción Blanda 1 penalizar si el profesor prefiere no dictar esa clase
        if id_franja in prof.franjas_no_disponibles:
            costo += 5
        #Restricción Blanda 2 penalizar si supera n clases consecutivas
        costo += self.penalizacion_consecutivas(estado, franja_nueva, max_consecutivas=2)

        horas_sobrantes = franja_nueva.duracion() - var.curso.duracion
        if horas_sobrantes > 0:
            costo += int(horas_sobrantes * 2)

        #saturación el mismo día
        clases_ese_dia = sum(
            1 for _,_,id_franja,_ in estado

            if self.mapa_franjas[id_franja].dia == franja_nueva.dia

        )
        if clases_ese_dia >= 2:
            costo += 3
        
        return costo

    def penalizacion_consecutivas(self,estado,franja_nueva, max_consecutivas=2):
        franjas_dia = [
            self.mapa_franjas[id_f]
            for _, _, id_f, _ in estado
            if self.mapa_franjas[id_f].dia == franja_nueva.dia
        ]
        franjas_dia.append(franja_nueva)
        franjas_dia.sort(key=lambda f: f.inicio_minutos())
        consecutivas = 1
        max_seguidas = 1
        for i in range(1, len(franjas_dia)):
            if franjas_dia[i].inicio_minutos() == franjas_dia[i - 1].fin_minutos():
                consecutivas +=1
                max_seguidas = max(max_seguidas, consecutivas)
            else:
                consecutivas = 1
        return 4 if max_seguidas > max_consecutivas else 0


    def heuristica(self, estado):
        #Heurística base para A*: cantidad de clases que faltan por asignar
        #Es admisible porque asume un costo mínimo de 1 por cada clase restante
        return len(self.variables_curso) - len(estado)
    


