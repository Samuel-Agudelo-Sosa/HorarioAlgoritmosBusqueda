# Sistema de Programación Académica Universitaria (UCTP)

Este proyecto resuelve el Problema de Asignación de Horarios Universitarios (UCTP - *University Course Timetabling Problem*) modelándolo como un Problema de Satisfacción de Restricciones (CSP). Utiliza algoritmos de búsqueda en espacios de estados para asignar materias, profesores, aulas y franjas horarias minimizando conflictos y penalizaciones.

## 🚀 Cómo ejecutar el proyecto

1. **Requisitos:** 
   - Python 3.8 o superior.
   - El módulo `tkinter` instalado (suele venir por defecto con Python; en Linux puedes requerir instalar `python3-tk`).
   - No requiere dependencias externas ni entornos virtuales complejos (solo librerías estándar).

2. **Ejecución:**
   Abre una terminal en el directorio raíz del proyecto y ejecuta el archivo principal:
   ```bash
   python main.py
   ```
   *(Nota: Asegúrate de ejecutar el archivo que inicializa la vista, por ejemplo `main.py` o `VistaHorario.py`).*

3. **Uso de la interfaz:**
   - Carga los cuatro archivos `.txt` desde el panel superior.
   - Selecciona el algoritmo deseado (Amplitud, Profundidad Iterativa, Costo Uniforme o A*).
   - Ajusta el número máximo de clases consecutivas (parámetro $N$).
   - Presiona **Generar Horario**.

---

## 📂 Formato de los Archivos de Entrada (.txt)

El sistema lee los datos desde archivos de texto plano separados por comas (`,`). Para garantizar que el programa los reconozca correctamente, debes seguir esta sintaxis estricta (sin espacios innecesarios antes o después de las comas):

### 1. `cursos.txt`
Define las materias a programar.
* **Sintaxis:** `ID_Curso,Nombre_del_Curso,Duración_en_horas`
* **Ejemplo:**
  ```text
  C01,Calculo,4
  C02,Fisica,3
  C04,Taller de Ingenieria,2
  ```

### 2. `franjas.txt`
Define los bloques de tiempo disponibles en la semana.
* **Sintaxis:** `Día,Hora_Inicio,Hora_Fin` (Formato 24h)
* **Ejemplo:**
  ```text
  Lunes,07:00,11:00
  Lunes,14:00,17:00
  Martes,08:00,12:00
  ```

### 3. `salones.txt`
Lista de aulas físicas disponibles.
* **Sintaxis:** `ID_Salon`
* **Ejemplo:**
  ```text
  S101
  S102
  ```

### 4. `profesores.txt`
Define a los docentes, qué materias pueden dictar y qué franjas bloquean por preferencia.
* **Sintaxis:** `ID_Profesor,Nombre,Cursos_Permitidos(separados por ;),Franjas_No_Preferidas(opcional, separadas por ;)`
* **Formato de la franja no preferida:** `Dia_HoraInicio_HoraFin`
* **Ejemplo:**
  ```text
  P01,Jair,C01;C05,Lunes_07:00_11:00
  P02,William,C02;C01;C08,Miercoles_06:00_10:00;Lunes_07:00_11:00
  P04,Joshua,C03;C06;C07;C08
  ```
  *(Nota: Si un profesor no tiene restricciones de horario, simplemente omite la cuarta columna como en el caso de Joshua).*

---

## ⚙️ Detalles Técnicos y Arquitectura

Este motor de búsqueda fue construido desde cero aplicando principios SOLID y el patrón arquitectónico **MVC (Modelo-Vista-Controlador)**, garantizando la separación estricta entre la interfaz gráfica (Tkinter) y la lógica matemática de inteligencia artificial.

### Técnicas CSP Implementadas
* **Ruptura de Simetrías (Round-Robin):** Se implementó una selección circular para la asignación de salones. Como todas las aulas son equivalentes para un único grupo, el algoritmo asigna la primera disponible y poda las permutaciones redundantes, reduciendo drásticamente el factor de ramificación exponencial ($3^n$).
* **Heurística MRV (Minimum Remaining Values):** En el preprocesamiento, los cursos se ordenan de mayor a menor duración y por la menor cantidad de profesores candidatos. Esto asegura que las variables más restringidas se ubiquen en los niveles superiores del árbol.
* **Heurística LCV (Least Constraining Value):** Las franjas horarias se evalúan de menor a mayor capacidad disponible, reservando los bloques de tiempo extensos para los cursos que genuinamente requieren mayor duración.

### Algoritmos de Búsqueda Soporte
El núcleo expone una clase base abstracta `BusquedaPrimeroMejor` que permite inyectar dinámicamente la función de evaluación `f(n)`:
1. **Amplitud (BFS) y Profundidad Iterativa (IDDFS):** Estrategias de búsqueda no informada que encuentran la solución topológica sin optimizar restricciones blandas.
2. **Costo Uniforme (UCS):** Búsqueda óptima que minimiza la función de costo $g(n)$, encargada de penalizar las franjas no preferidas por los profesores y la superación del límite $N$ de clases consecutivas.
3. **A* (A-Star):** Búsqueda heurística que combina $g(n)$ con $h(n)$ (estimación de variables restantes). Utiliza un sistema de desempate en la cola de prioridad basado en la profundidad `(f, h)` para acelerar la convergencia hacia el estado meta sin perder optimalidad.