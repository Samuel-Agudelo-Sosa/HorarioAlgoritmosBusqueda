import tkinter as tk
# ttk (Themed Tkinter): Módulo con widgets modernos y estilizados (botones, tablas, combos).
# filedialog: Permite abrir el explorador de archivos del sistema operativo.
# messagebox: Genera ventanas emergentes de alerta, información o error.
from tkinter import ttk, filedialog, messagebox


class VistaHorario:
    def __init__(self, root, controlador):
        # 'root' es la ventana raíz o principal de toda la interfaz gráfica.
        self.root = root
        self.controlador = controlador

        # Define el título que aparece en la barra superior de la ventana.
        self.root.title("Sistema de Programación Académica Universitaria - CSP")


        # Primero solicitamos al sistema operativo que maximice la ventana. A diferencia de
        # fullscreen, '-zoomed' respeta las barras del sistema (dock lateral y barra superior)
        # y mantiene visible el botón de minimizar para cambiar entre aplicaciones.
        try:
            self.root.attributes("-zoomed", True)  # Para entornos Linux (Ubuntu/GNOME)
        except tk.TclError:
            self.root.state("zoomed")              # Para entornos Windows

        # update(): Fuerza a Tkinter a procesar el maximizado inmediatamente para poder
        # leer las dimensiones reales del área libre (descontando la barra de tareas).
        self.root.update()

        ancho_util = self.root.winfo_width()
        alto_util = self.root.winfo_height()
        pos_x = self.root.winfo_x()
        pos_y = self.root.winfo_y()

        # Si el gestor de ventanas aún no aplicó el maximizado (ancho <= 200 px por defecto),
        # calculamos manualmente el espacio libre descontando ~75 px del dock izquierdo y ~35 px arriba.
        if ancho_util <= 200:
            ancho_util = self.root.winfo_screenwidth() - 75
            alto_util = self.root.winfo_screenheight() - 35
            pos_x, pos_y = 75, 35

        # geometry("ANCHO x ALTO + X + Y"): Fija exactamente el tamaño y posición dentro del área libre.
        self.root.geometry(f"{ancho_util}x{alto_util}+{pos_x}+{pos_y}")

        # resizable(ancho, alto): Al pasar (False, False) después de ajustar el tamaño útil,
        # se impide que la ventana pueda achicarse arrastrando bordes (protegiendo el panel
        # inferior de estadísticas), pero se conserva intacto el botón de minimizar.
        self.root.resizable(False, False)

        # configure(bg=...): Define el color de fondo general de la ventana principal.
        self.root.configure(bg="#F4F6F9")

        # Construcción ordenada de cada sección visual de la interfaz
        self.configurar_estilos()
        self.crear_encabezado()
        self.crear_panel_carga()
        self.crear_panel_configuracion()
        self.crear_panel_horario()
        self.crear_panel_estadisticas()

    def configurar_estilos(self):
        # ttk.Style() centraliza la apariencia visual (colores, fuentes, bordes) de los widgets ttk.
        style = ttk.Style()

        # 'clam' es un tema visual plano y moderno que permite personalizar colores fácilmente
        style.theme_use("clam")

        # Paleta de colores institucionales en formato hexadecimal
        AZUL_PRIMARIO = "#1E3A5F"
        AZUL_OSCURO = "#152944"
        FONDO = "#F4F6F9"
        BLANCO = "#FFFFFF"
        BORDE = "#CBD5E1"


        # 'background': Color de FONDO del componente.
        # 'foreground': Color del TEXTO o contenido frontal del componente.
        style.configure("TFrame", background=FONDO)


        # 'relief': Define el estilo del borde
        style.configure("TLabelframe", background=FONDO, bordercolor=BORDE, relief="solid")
        style.configure("TLabelframe.Label", background=FONDO, foreground=AZUL_PRIMARIO,
                        font=("Segoe UI", 10, "bold"))
        style.configure("TLabel", background=FONDO, foreground="#1E293B", font=("Segoe UI", 9))

        # 'padding': Margen INTERNO entre el borde del widget y su texto/contenido.
        # padding=(10, 5) aplica 10 píxeles a izquierda/derecha y 5 píxeles arriba/abajo.
        style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=(10, 5),
                        background="#E2E8F0", foreground="#1E293B")

        # Creamos un estilo personalizado llamado "Primario.TButton" heredando de "TButton"
        style.configure("Primario.TButton", font=("Segoe UI", 10, "bold"), padding=(16, 6),
                        background=AZUL_PRIMARIO, foreground=BLANCO)

        # map(): Cambia propiedades dinámicamente según el estado del mouse/widget
        # ("active" aplica cuando el cursor pasa encima o se presiona el botón).
        style.map("Primario.TButton", background=[("active", AZUL_OSCURO)])

        # Estilo de las celdas y filas de la tabla principal del horario
        style.configure("Horario.Treeview",
                        background=BLANCO,
                        foreground="#0F172A",
                        fieldbackground=BLANCO, # Color de fondo del área vacía de la tabla
                        rowheight=54,           # Altura en píxeles de cada fila (espacio para 3 líneas de texto)
                        bordercolor=BORDE,
                        lightcolor=BORDE,
                        darkcolor=BORDE,
                        font=("Segoe UI", 9))

        # Estilo de los encabezados (títulos de columnas) de la tabla del horario
        style.configure("Horario.Treeview.Heading",
                        background=AZUL_PRIMARIO,
                        foreground=BLANCO,
                        relief="raised", # Efecto elevado en los encabezados de columna
                        bordercolor=AZUL_OSCURO,
                        font=("Segoe UI", 9, "bold"))
        style.map("Horario.Treeview.Heading", background=[("active", AZUL_OSCURO)])

        # Estilo de la tabla inferior de estadísticas (filas más delgadas: rowheight=26)
        style.configure("Stats.Treeview",
                        background=BLANCO,
                        foreground="#0F172A",
                        fieldbackground=BLANCO,
                        rowheight=26,
                        bordercolor=BORDE,
                        lightcolor=BORDE,
                        darkcolor=BORDE,
                        font=("Segoe UI", 9))
        style.configure("Stats.Treeview.Heading",
                        background="#334155",
                        foreground=BLANCO,
                        font=("Segoe UI", 9, "bold"))

    def crear_encabezado(self):
        # tk.Frame: Contenedor rectangular básico usado aquí como banner superior.
        # padx y pady dentro del Frame actúan como relleno interno.
        banner = tk.Frame(self.root, bg="#1E3A5F", pady=10, padx=16)

        # pack(): Gestor de geometría que apila bloques vertical u horizontalmente.
        # fill="x" estira el banner a todo lo ancho de la ventana.
        banner.pack(fill="x")

        # side="left" y side="right" alinean las etiquetas a los extremos opuestos del banner.
        tk.Label(banner, text="Programación Académica Universitaria",
                 bg="#1E3A5F", fg="white", font=("Segoe UI", 14, "bold")).pack(side="left")
        tk.Label(banner, text="Satisfacción de Restricciones (CSP)",
                 bg="#1E3A5F", fg="#CBD5E1", font=("Segoe UI", 10)).pack(side="right")

    def crear_panel_carga(self):
        # ttk.LabelFrame: Contenedor con borde y un título incrustado en la parte superior.
        frame = ttk.LabelFrame(self.root, text=" 1. Carga de Archivos de Entrada ", padding=(14, 8))
        # padx y pady en pack() definen el margen EXTERNO que separa este panel de sus vecinos.
        frame.pack(fill="x", padx=16, pady=(8, 4))

        # columnconfigure(1, weight=1): Indica que la columna 1 (donde va la ruta del archivo)
        # absorberá todo el espacio horizontal sobrante, empujando la columna 2 al borde derecho.
        frame.columnconfigure(1, weight=1)

        self.rutas_vars = {}
        self.estados_labels = {}

        archivos_info = [
            ("profesores", "Cargar profesores.txt"),
            ("cursos", "Cargar cursos.txt"),
            ("salones", "Cargar salones.txt"),
            ("franjas", "Cargar franjas.txt"),
        ]

        for i, (tipo, texto_btn) in enumerate(archivos_info):
            # tk.StringVar(): Variable observable de Tkinter. Al modificarla con .set(),
            # cualquier Label vinculado a ella actualiza su texto en pantalla automáticamente.
            self.rutas_vars[tipo] = tk.StringVar(value="Ningún archivo seleccionado")

            # lambda t=tipo: Captura el valor actual de 'tipo' en cada vuelta del ciclo;
            # sin 't=tipo', todos los botones terminarían enviando el último valor ("franjas").
            # grid(): Gestor de geometría en cuadrícula (filas y columnas).
            # sticky="w" (West/Oeste) alinea el elemento a la izquierda de su celda.
            ttk.Button(frame, text=texto_btn, width=22,
                       command=lambda t=tipo: self.pedir_archivo(t)).grid(row=i, column=0, pady=2, sticky="w")

            # textvariable vincula el texto del Label directamente con la StringVar
            ttk.Label(frame, textvariable=self.rutas_vars[tipo],
                      foreground="#475569").grid(row=i, column=1, padx=12, sticky="w")

            # sticky="e" (East/Este) alinea el estado a la derecha de su celda
            lbl_estado = tk.Label(frame, text="Pendiente", bg="#F4F6F9", fg="#94A3B8",
                                  font=("Segoe UI", 9, "bold"))
            lbl_estado.grid(row=i, column=2, padx=6, sticky="e")
            self.estados_labels[tipo] = lbl_estado

    def crear_panel_configuracion(self):
        frame = ttk.LabelFrame(self.root, text=" 2. Configuración de Búsqueda ", padding=(14, 8))
        frame.pack(fill="x", padx=16, pady=4)

        # Usamos un frame interno transparente para agrupar todos los controles a la izquierda y alinearlos verticalmente
        controles_izq = tk.Frame(frame, bg="#F4F6F9")
        controles_izq.pack(side="left", fill="y")

        # 1. Combobox Algoritmo
        ttk.Label(controles_izq, text="Algoritmo:").pack(side="left", pady=10)
        self.combo_algoritmo = ttk.Combobox(
            controles_izq,
            values=["Amplitud", "Profundidad Iterativa", "Costo Uniforme", "A*"],
            state="readonly",
            width=20
        )
        self.combo_algoritmo.current(0)
        self.combo_algoritmo.pack(side="left", padx=(6, 16), pady=10)

        # 2. Combobox Redundancia
        ttk.Label(controles_izq, text="Control de Redundancia:").pack(side="left", pady=10)
        self.combo_control = ttk.Combobox(
            controles_izq,
            values=[
                "0 - Sin control",
                "1 - Evitar devolverse",
                "2 - Evitar ciclos",
                "3 - Búsquedas en grafos"
            ],
            state="readonly",
            width=26
        )
        self.combo_control.current(3)
        self.combo_control.pack(side="left", padx=(6, 16), pady=10)

        # 3. Spinbox N (Clases Consecutivas) AHORA ALINEADO HORIZONTALMENTE
        ttk.Label(controles_izq, text="Máx. clases consecutivas (N):").pack(side="left", pady=10)
        self.spin_consecutivas = ttk.Spinbox(controles_izq, from_=1, to=5, width=5)
        self.spin_consecutivas.set(2)
        self.spin_consecutivas.pack(side="left", padx=(6, 16), pady=10)

        # 4. Botón Generar (Pegado a la derecha de los controles)
        ttk.Button(controles_izq, text="Generar Horario", style="Primario.TButton",
                   command=self.controlador.generar_horario).pack(side="left", padx=4, pady=10)

        # Botón Limpiar (Alineado al extremo derecho del panel principal)
        ttk.Button(frame, text="Limpiar Estadísticas",
                   command=self.limpiar_estadisticas).pack(side="right", pady=10)




    def crear_panel_horario(self):
        # fill="both" y expand=True permiten que el panel del horario aproveche el espacio
        # disponible en pantallas grandes sin empujar fuera de vista el panel inferior.
        frame = ttk.LabelFrame(self.root, text=" 3. Horario Generado ", padding=(12, 6))
        frame.pack(fill="both", expand=True, padx=16, pady=4)

        columnas = ("Hora", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado")

        # ttk.Scrollbar: Barras de desplazamiento vertical y horizontal para navegar la tabla
        scroll_y = ttk.Scrollbar(frame, orient="vertical")
        scroll_x = ttk.Scrollbar(frame, orient="horizontal")

        # ttk.Treeview: Widget tabular.
        # show="headings" oculta la columna inicial vacía de árbol (#0) y muestra solo nuestras columnas.
        # height=5 define cuántas filas visibles reserva por defecto, protegiendo el espacio de estadísticas.
        self.tabla_horario = ttk.Treeview(
            frame,
            columns=columnas,
            show="headings",
            height=5,
            style="Horario.Treeview",
            yscrollcommand=scroll_y.set, # Sincroniza la posición de la tabla con el scrollbar vertical
            xscrollcommand=scroll_x.set  # Sincroniza la posición de la tabla con el scrollbar horizontal
        )
        # Sincroniza el arrastre de las barras de desplazamiento con la vista de la tabla
        scroll_y.config(command=self.tabla_horario.yview)
        scroll_x.config(command=self.tabla_horario.xview)

        # tag_configure(): Crea etiquetas de estilo para alternar colores entre filas pares e impares
        self.tabla_horario.tag_configure("par", background="#FFFFFF")
        self.tabla_horario.tag_configure("impar", background="#F1F5F9")

        for col in columnas:
            ancho = 115 if col == "Hora" else 145
            self.tabla_horario.heading(col, text=col)  # Texto visible en el encabezado
            self.tabla_horario.column(col, width=ancho, minwidth=100, anchor="center")  # Alineación centrada


        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tabla_horario.pack(fill="both", expand=True)

    def crear_panel_estadisticas(self):
        frame = ttk.LabelFrame(self.root, text=" 4. Estadísticas de Ejecución ", padding=(12, 6))
        frame.pack(fill="x", padx=16, pady=(4, 12))

        columnas_stats = ("Algoritmo", "Redundancia", "Nodos", "Costo", "Tiempo", "Solución")
        scroll_y = ttk.Scrollbar(frame, orient="vertical")

        self.tabla_stats = ttk.Treeview(
            frame,
            columns=columnas_stats,
            show="headings",
            height=4,  # Muestra 4 ejecuciones simultáneamente; las demás se ven con scroll
            style="Stats.Treeview",
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.tabla_stats.yview)

        for col in columnas_stats:
            self.tabla_stats.heading(col, text=col)
            self.tabla_stats.column(col, width=140, anchor="center")

        scroll_y.pack(side="right", fill="y")
        self.tabla_stats.pack(fill="x", expand=True)

    def pedir_archivo(self, tipo):
        # askopenfilename(): Abre el selector nativo filtrando únicamente archivos .txt
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if ruta:
            self.rutas_vars[tipo].set(ruta)
            self.estados_labels[tipo].config(text="✓ Cargado", fg="#15803D")
            self.controlador.registrar_archivo(tipo, ruta)

    def mostrar_error(self, mensaje):
        # Muestra una ventana modal de error que bloquea la interacción hasta pulsar OK
        messagebox.showerror("Error", mensaje)

    

    def actualizar_horario(self, filas_horario):
        # --- EXPLICACIÓN DEL ASTERISCO (*) ---
        # `get_children()` retorna una tupla con los IDs internos de todas las filas actuales,
        # El operador `*` desempaqueta la tupla en argumentos individuales para vaciar toda la tabla.
        self.tabla_horario.delete(*self.tabla_horario.get_children())

        for idx, fila in enumerate(filas_horario):
            tag = "par" if idx % 2 == 0 else "impar"
            # insert("", "end", ...): Inserta en la raíz ("") al final de la tabla ("end")
            self.tabla_horario.insert("", "end", values=fila, tags=(tag,))

    def agregar_estadistica(self, stats):
        # Agrega una fila al final de la tabla de estadísticas con la tupla de 6 valores:
        # (algoritmo, redundancia, nodos, costo, tiempo, solucion)
        self.tabla_stats.insert("", "end", values=stats)

    def limpiar_estadisticas(self):
        # Desempaqueta todos los IDs de filas de estadísticas con `*` y los elimina
        self.tabla_stats.delete(*self.tabla_stats.get_children())