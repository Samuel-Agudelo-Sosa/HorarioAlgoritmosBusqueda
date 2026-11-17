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
        nivel_control = int(self.vista.combo_control.get().split(" - ")[0])
        max_consecutivas = int(self.vista.spin_consecutivas.get())


        try:
            variables, franjas, salones = GestorArchivos.cargar_todo(self.archivos)
            problema = Horario(variables, franjas, salones, max_consecutivas = max_consecutivas)

            if "Amplitud" in algoritmo_seleccionado:
                algoritmo = Amplitud(control=nivel_control)
            elif "Costo Uniforme" in algoritmo_seleccionado:
                algoritmo = CostoUniforme(control=nivel_control)
            elif "Profundidad Iterativa" in algoritmo_seleccionado:
                algoritmo = ProfundidadIterativa(limite_maximo=float('inf'), control=nivel_control)
            elif "A*" in algoritmo_seleccionado:
                algoritmo = AEstrella(control=nivel_control)

            inicio = time.perf_counter()
            solucion_nodo = algoritmo.busqueda(problema)
            fin = time.perf_counter()
            tiempo_segundos = f"{(fin - inicio):.4f}s"

            if solucion_nodo:
                filas_horario = self.formatear_horario(solucion_nodo.estado, problema)
                self.vista.actualizar_horario(filas_horario)
                solucion_texto = "Sí"
                # Extraemos el costo del nodo solución 
                costo_texto = f"{solucion_nodo.g:.2f}" 
            else:
                self.vista.actualizar_horario([])
                solucion_texto = "No"
                costo_texto = "N/A"
                self.vista.mostrar_error("No se encontró ninguna solución válida.")

            # Obtenemos el texto seleccionado en el combo de control de redundancia
            redundancia_seleccionada = self.vista.combo_control.get()

            self.vista.agregar_estadistica((
                algoritmo_seleccionado,
                redundancia_seleccionada,
                algoritmo.nodos_evaluados,
                costo_texto,
                tiempo_segundos,
                solucion_texto
            ))
        except Exception as e:          
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

        for id_var,id_profesor, id_franja, id_salon in estado:
            var = problema.mapa_variables[id_var]
            prof = problema.mapa_profesores[id_profesor]
            franja = problema.mapa_franjas[id_franja]
            clave_hora = f"{franja.inicio} - {franja.fin}"

            dia_norm = franja.dia.lower().replace("é", "e").replace("á","a")
            if dia_norm in dias_columnas and clave_hora in grilla:
                col_idx = dias_columnas.index(dia_norm)
                grilla[clave_hora][col_idx] = f"{var.curso.nombre}\n{prof.nombre}\n{id_salon}"

        filas = []
        for hora in horas_ordenadas:
            filas.append((hora, *grilla[hora]))
        return filas

