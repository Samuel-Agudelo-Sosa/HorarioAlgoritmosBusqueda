 # test_carga.py
import os
from backend.core.logica.GestorArchivos import GestorArchivos
from backend.core.modelos.VariableCurso import VariableCurso

def probar_sistema():
    # 1. Definir rutas relativas a los archivos de prueba
    ruta_base = os.path.join(os.path.dirname(__file__), 'datos')
    f_cursos = os.path.join(ruta_base, 'cursos.txt')
    f_profes = os.path.join(ruta_base, 'profesores.txt')
    f_salones = os.path.join(ruta_base, 'salones.txt')
    f_franjas = os.path.join(ruta_base, 'franjas.txt')

    print("--- 1. CARGANDO ARCHIVOS ---")
    cursos = GestorArchivos.cargar_cursos(f_cursos)
    profesores = GestorArchivos.cargar_profesores(f_profes)
    salones = GestorArchivos.cargar_salones(f_salones)
    franjas = GestorArchivos.cargar_franjas(f_franjas)

    print(f"Cursos cargados ({len(cursos)}): {cursos}")
    print(f"Profesores cargados ({len(profesores)}): {profesores}")
    print(f"Salones cargados ({len(salones)}): {salones}")
    print(f"Franjas cargadas ({len(franjas)}): {franjas}\n")

    print("--- 2. PRUEBA DE CRUCE DE FRANJAS ---")
    if len(franjas) >= 2:
        f1 = franjas[0]
        f2 = franjas[1]
        cruza = f1.se_cruza_con(f2)
        print(f"¿Se cruzan '{f1}' y '{f2}'?: {cruza}")

    print("\n--- 3. GENERANDO VARIABLES DEL CSP ---")
    variables = []
    contador = 1
    
    # Emparejar cada curso con el profesor correspondiente
    for curso in cursos:
        prof_encontrado = None
        for prof in profesores:
            if curso.id_curso in prof.id_cursos:
                prof_encontrado = prof
                break
        
        if prof_encontrado:
            var = VariableCurso(f"V{contador}", curso, prof_encontrado)
            variables.append(var)
            contador += 1
        else:
            print(f"[ERROR] El curso {curso.nombre} ({curso.id_curso}) no tiene profesor asignado.")

    print(f"Variables a programar en el horario ({len(variables)}):")
    for v in variables:
        print(f"  - {v}")

if __name__ == '__main__':
    probar_sistema()