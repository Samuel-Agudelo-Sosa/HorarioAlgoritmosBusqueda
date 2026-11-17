import tkinter as tk
from frontend.ControladorHorario import ControladorHorario
from frontend.VistaHorario import VistaHorario

def main():
    # 1. Crear ventana principal
    root = tk.Tk()
    
    # 2. Instanciar Controlador
    controlador = ControladorHorario()
    
    # 3. Instanciar Vista y pasarle el controlador
    vista = VistaHorario(root, controlador)
    
    # 4. Conectar la vista al controlador
    controlador.set_vista(vista)
    
    # 5. Iniciar la aplicación
    root.mainloop() #bucle infinito que congela el código ahí en la aplicación

if __name__ == "__main__":
    main()