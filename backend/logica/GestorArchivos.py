import os
from backend.modelos.Curso import Curso
from backend.modelos.Profesor import Profesor
from backend.modelos.Salon import Salon
from backend.modelos.Franja import Franja
from backend.modelos.VariableCurso import VariableCurso


class GestorArchivos:

    @staticmethod
    def cargar_cursos(ruta_archivo):
        cursos = []
        ids_vistos = set()
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            for linea in file:
                linea_limpia = linea.strip()
                if not linea_limpia:
                    continue
                datos = linea_limpia.split(',')
                if len(datos) == 3:
                    id_curso = datos[0].strip()
                    nombre = datos[1].strip()
                    duracion = int(datos[2].strip())
                    if id_curso in ids_vistos:
                        print(f"[Advertencia] Curso duplicado omitido en línea: {id_curso}")
                        continue
                    if duracion < 2:
                        print(f"La duración del curso {nombre} debe ser mínimo de 2 horas")
                    ids_vistos.add(id_curso)
                    cursos.append(Curso(id_curso, nombre, duracion))
        return cursos

    @staticmethod
    def cargar_profesores(ruta_archivo):
        profesores = []
        ids_vistos = set()
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            for linea in file:
                linea_limpia = linea.strip()
                if not linea_limpia:
                    continue
                datos = linea_limpia.split(',')
                if len(datos) == 3:
                    id_profesor = datos[0].strip()
                    nombre = datos[1].strip()
                    if id_profesor in ids_vistos:
                        print(f"[Advertencia] Profesor duplicado omitido: {id_profesor}")
                        continue

                    cursos_limpios  = datos[2].strip()
                    cursos = [c.strip() for c in cursos_limpios.split(';') if c.strip()] if cursos_limpios else []
                    if not cursos:
                        print(f"[Advertencia] El profesor {nombre}  {id_profesor} fue omitido por no tener cursos asignados")
                        continue
                    ids_vistos.add(id_profesor)
                    profesores.append(Profesor(id_profesor, nombre, cursos))
        return profesores


    @staticmethod
    def cargar_salones(ruta_archivo):
        salones = []
        ids_vistos = set()
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            for linea in file:
                id_salon = linea.strip()
                if id_salon: #comprueba línea no vacía
                    if id_salon in ids_vistos:
                        print(f"[Advertencia] Salón duplicado omitido: {id_salon}")
                        continue
                    ids_vistos.add(id_salon)
                    salones.append(Salon(id_salon))
        return salones


    @staticmethod
    def cargar_franjas(ruta_archivo):
        franjas = []
        ids_vistos = set()
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            for linea in file:
                linea_limpia = linea.strip()
                if not linea_limpia:
                    continue
                datos = linea_limpia.split(',')
                if len(datos) == 3:
                    dia = datos[0].strip()
                    hora_inicial = datos[1].strip()
                    hora_final = datos[2].strip()
                    # Instancia temporal para validar minutos
                    f_temp = Franja(dia, hora_inicial, hora_final)
                
                    # Validación: la hora final debe ser estrictamente mayor a la inicial
                    if f_temp.fin_minutos() <= f_temp.inicio_minutos():
                        print(f"[Advertenci Franja inválida omitida ({dia} {hora_inicial}-{hora_final}): la hora final debe ser posterior a la hora inicial (revisa si falta formato 24h, ej. 17:00).")
                        continue
                    clave_franja = f"{dia.lower()}_{hora_inicial}_{hora_final}"
                    if clave_franja in ids_vistos:
                        print(f"[Advertencia] Franja duplicada omitida: {dia} {hora_inicial}-{hora_final}")
                        continue
                    ids_vistos.add(clave_franja)
                    franjas.append(f_temp)
              
        return franjas


    @staticmethod
    def generar_variables_csp(cursos, profesores):
        variables = []
        mapa_cursos = {c.id_curso: c for c in cursos}
        cursos_asignados = set()
        id_var = 0

        for prof in profesores:
            for id_curso in prof.id_cursos:
                if id_curso not in mapa_cursos:
                    print(f"[Advertencia] el curso {id_curso} del prof. {prof.nombre} no existe en cursos.txt")
                    continue
                if id_curso in cursos_asignados:
                    print(f"[Advertencia] El curso {id_curso} ya tiene profesor asignado")
                    continue
                variables.append(VariableCurso(id_var, mapa_cursos[id_curso], prof))
                cursos_asignados.add(id_curso)
                id_var += 1

        if len(cursos_asignados) < len(cursos):
            faltantes = set(mapa_cursos.keys()) - cursos_asignados
            raise ValueError(f"Los siguientes cursos no tienen profesor asignado {', '.join(faltantes)}")

        return variables


    @staticmethod
    def cargar_todo(rutas_archivos):
        cursos = GestorArchivos.cargar_cursos(rutas_archivos["cursos"])
        profesores = GestorArchivos.cargar_profesores(rutas_archivos["profesores"])
        salones = GestorArchivos.cargar_salones(rutas_archivos["salones"])
        franjas = GestorArchivos.cargar_franjas(rutas_archivos["franjas"])
        variables_curso = GestorArchivos.generar_variables_csp(cursos, profesores)
        return variables_curso, franjas, salones
                