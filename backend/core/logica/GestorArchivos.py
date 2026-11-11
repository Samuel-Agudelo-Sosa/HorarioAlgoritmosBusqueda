import os
from backend.core.modelos.Curso import Curso
from backend.core.modelos.Profesor import Profesor
from backend.core.modelos.Salon import Salon
from backend.core.modelos.Franja import Franja
from backend.core.modelos.VariableCurso import VariableCurso


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
