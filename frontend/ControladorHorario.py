import time
import traceback
from backend.logica.GestorArchivos import GestorArchivos
from backend.logica.Horario import Horario
from backend.core.algoritmos.Amplitud import Amplitud
from backend.core.algoritmos.CostoUniforme import CostoUniforme
from backend.core.algoritmos.ProfundidadIterativa import ProfundidadIterativa
from backend.core.algoritmos.AEstrella import AEstrella


class ControladorHorario:
    def __init__(self):
        self.vista = None
        self.archivos = {"profesores": "", "cursos": "", "salones": "", "franjas": ""}

    def set_vista(self, vista):
        self.vista = vista

    def registrar_archivo(self, tipo, ruta):
        self.archivos[tipo] = ruta

    def generar_horario(self):
        #validar que todos los archivos estén cargados
        if any(ruta == "" for ruta in self.archivos.values()):
            self.vista.mostrar_error("Debe cargar los 4 archivos antes de generar el horario")
            return

        algoritmo_seleccionado = self.vista.combo_algoritmo.get()

        try:
            variables, franjas, salones = GestorArchivos.cargar_todo(self.archivos)
            problema = Horario(variables, franjas, salones)

            if "Amplitud" in algoritmo_seleccionado:
                algoritmo = Amplitud(control=3)
            elif "Costo Uniforme" in algoritmo_seleccionado:
                algoritmo = CostoUniforme(control=3)
            elif "Profundidad Iterativa" in algoritmo_seleccionado:
                algoritmo = ProfundidadIterativa(limite_maximo=20, control=3)
            elif "A*" in algoritmo_seleccionado:
                algoritmo = AEstrella(control=3)

            inicio = time.perf_counter()
            solucion_nodo = algoritmo.busqueda(problema)
            fin = time.perf_counter()
            tiempo_segundos = f"{(fin - inicio):.4f}s"

            if solucion_nodo:
                filas_horario = self.formatear_horario(solucion_nodo.estado, problema)
                self.vista.actualizar_horario(filas_horario)
                solucion_texto = "Sí"

            else:
                self.vista.actualizar_horario([])
                solucion_texto = "No"
                self.vista.mostrar_error("No se encontró ninguna solución válida.")

            self.vista.agregar_estadistica((
                algoritmo_seleccionado,
                algoritmo.nodos_evaluados,
                tiempo_segundos,
                solucion_texto
            ))
        except Exception as e:          
            import traceback
            traceback.print_exc()  # Muestra en la consola exactamente en qué archivo y línea ocurrió
            self.vista.mostrar_error(f"Error al ejecutar: {str(e)}")

    def formatear_horario(self, estado, problema):

        dias_columnas = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado"]
        bloques_unicos = {}
        for f in problema.franjas:
            clave_hora = f"{f.inicio} - {f.fin}"
            bloques_unicos[clave_hora] = f.inicio_minutos()
        horas_ordenadas = sorted(bloques_unicos.keys(), key=lambda h: bloques_unicos[h])
        grilla = {hora: [""] * 6 for hora in horas_ordenadas}

        for id_var, id_franja, id_salon in estado:
            var = problema.mapa_variables[id_var]
            franja = problema.mapa_franjas[id_franja]
            clave_hora = f"{franja.inicio} - {franja.fin}"

            dia_norm = franja.dia.lower().replace("é", "e").replace("á","a")
            if dia_norm in dias_columnas and clave_hora in grilla:
                col_idx = dias_columnas.index(dia_norm)
                grilla[clave_hora][col_idx] = f"{var.curso.nombre}\n{var.profesor.nombre}\n{id_salon}"

        filas = []
        for hora in horas_ordenadas:
            filas.append((hora, *grilla[hora]))
        return filas

