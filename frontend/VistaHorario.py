import tkinter as tk
from tkinter import ttk, filedialog, messagebox

 

class VistaHorario:
    def __init__(self, root, controlador):
        self.root = root #ventana principal
        self.controlador = controlador
        self.root.title("Programación Académica Universitaria")
        self.root.geometry("900x700")

        self.crear_panel_carga()
        self.crear_panel_configuracion()
        self.crear_panel_horario()
        self.crear_panel_estadisticas()
        


    def crear_panel_carga(self):
        #Crea un contenedor con bode y título en la parte superior
        frame = ttk.LabelFrame(self.root, text="Carga de Archivos", padding=10)
        frame.pack(fill="x", padx=10, pady=5) #Fill x ocupa todo el ancho disponible

        #permiten actualizar el texto de las etiquetas cuando cambio su valor
        self.rutas_vars = {
            "profesores": tk.StringVar(value="Ruta: Ninguna"),
            "cursos": tk.StringVar(value="Ruta: Ninguna"),
            "salones": tk.StringVar(value="Ruta: Ninguna"),
            "franjas": tk.StringVar(value="Ruta: Ninguna")
        }

        #iterar sobre los 4 tipos de archivos
        for i, tipo in enumerate(["profesores", "cursos", "salones", "franjas"]):
            ttk.Button(frame,
                       text=f"Cargar {tipo}.txt",
                       command=lambda t=tipo: self.pedir_archivo(t)
                       ).grid(row=i,column=0, pady=2, sticky="w") #alinea a la izquierda (west)
            ttk.Label(frame, textvariable=self.rutas_vars[tipo]).grid(row=i, column=1, padx=10, sticky="w")


    def crear_panel_configuracion(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="Algoritmo:").pack(side="left")

        self.combo_algoritmo = ttk.Combobox(
            frame,
            values=["Amplitud", "Profundidad Iterativa", "Costo Uniforme", "A*"],
            state="readonly" #usuario no escriba texto libre
        )

        self.combo_algoritmo.current(0) #selecciona por defecto primer elemento
        self.combo_algoritmo.pack(side="left", padx=10)

        #Botón que delega la ejecución directamente al método del controlador
        ttk.Button(frame, text="Generar Horario", command=self.controlador.generar_horario).pack(side="left")



    def crear_panel_horario(self):
        frame = ttk.LabelFrame(self.root, text="Horario Generado", padding=10)
        #fill both permite que la tabla crezca si el usuario maximiza la ventana
        frame.pack(fill="both", expand=True, padx=10, pady=5) 

        #Definición de los identificadores de las columnas
        columnas = ("Hora", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado")
        style = ttk.Style()
        style.configure("Treeview", rowheight=55)
        #Muestra exclusivamente las columnas 
        self.tabla_horario = ttk.Treeview(frame, columns=columnas, show="headings", height=10)

        #Configura el encabezado visible y las dimensiones de cada columna:
        for col in columnas:
            self.tabla_horario.heading(col, text=col)
            self.tabla_horario.column(col, width=120, anchor="center")

        self.tabla_horario.pack(fill="both", expand=True)


    def crear_panel_estadisticas(self):
        frame = ttk.LabelFrame(self.root, text="Estadisticas", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        columnas_stats = ("Algoritmo", "Nodos", "Tiempo", "Solucion")
        self.tabla_stats = ttk.Treeview(frame, columns=columnas_stats, show="headings", height=4)

        for col in columnas_stats:
            self.tabla_stats.heading(col, text=col)
            self.tabla_stats.column(col, width=150, anchor="center")

        self.tabla_stats.pack(fill="x")

    #interfaz comunicación con el controlador:

    def pedir_archivo(self, tipo):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto","*.txt")])
        if ruta: #veritifca que no se cierre la ventana sin elegir algo
            self.rutas_vars[tipo].set(f"Ruta: {ruta}")
            self.controlador.registrar_archivo(tipo, ruta)

    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)

    def actualizar_horario(self, filas_horario):
        #elimina filas actuales
        self.tabla_horario.delete(*self.tabla_horario.get_children())

        for fila in filas_horario:
            self.tabla_horario.insert("", "end", values=fila)


    def agregar_estadistica(self, stats):
        #agrega filas sin borrar ejecuciones anteriores
        self.tabla_stats.insert("", "end", value=stats)
