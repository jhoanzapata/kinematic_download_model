import tkinter as tk
from tkinter import ttk, messagebox
import threading
from src.simulator import SimuladorDescarga  # Cambiado
from src.logger import setup_logger
from src.reporter import guardar_reporte
from src.simulator import calcular_parametros_fisicos  # Cambiado

class AppSimulador:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Descargas Profesional")
        self.logger = setup_logger()

        # Variables
        self.velocidad_var = tk.StringVar()
        self.tamano_var = tk.StringVar()

        # Interfaz
        ttk.Label(root, text="Velocidad (Mbps):").grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(root, textvariable=self.velocidad_var).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(root, text="Tamaño (GB):").grid(row=1, column=0, padx=10, pady=5)
        ttk.Entry(root, textvariable=self.tamano_var).grid(row=1, column=1, padx=10, pady=5)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        ttk.Button(root, text="Iniciar Simulación", command=self.iniciar_simulacion).grid(row=3, column=0, columnspan=2, pady=10)

        self.resultado = tk.Text(root, height=8, width=50)
        self.resultado.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def iniciar_simulacion(self):
        try:
            velocidad = float(self.velocidad_var.get())
            tamano = float(self.tamano_var.get())
            if velocidad <= 0 or tamano <= 0:
                raise ValueError("Valores inválidos.")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores válidos y positivos.")
            return

        # Ejecutar en hilo separado para no bloquear la GUI
        thread = threading.Thread(target=self._ejecutar_simulacion, args=(velocidad, tamano))
        thread.start()

    def _ejecutar_simulacion(self, velocidad, tamano):
        vel_mbs, total_mb, tiempo_seg = calcular_parametros_fisicos(velocidad, tamano)
        simulador = SimuladorDescarga(total_mb, vel_mbs, self.logger)
        inicio, fin = simulador.iniciar(100.0)
        self._mostrar_resultado(inicio, fin, tiempo_seg)

    def _mostrar_resultado(self, inicio, fin, tiempo_seg):
        minutos = int(tiempo_seg // 60)
        segundos = int(tiempo_seg % 60)
        texto = f"--- Reporte Final ---\n"
        texto += f"Hora inicio: {inicio.strftime('%H:%M:%S')}\n"
        texto += f"Hora fin: {fin.strftime('%H:%M:%S')}\n"
        texto += f"Tiempo teórico: {minutos}m {segundos}s\n"
        texto += f"Duración simulación: {fin - inicio}\n"

        self.resultado.delete(1.0, tk.END)
        self.resultado.insert(tk.END, texto)

        # Guardar reporte
        guardar_reporte(inicio, fin, tiempo_seg)

def main():
    root = tk.Tk()
    app = AppSimulador(root)
    root.mainloop()

if __name__ == "__main__":
    main()