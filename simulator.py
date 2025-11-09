import datetime
import time
import signal
from tqdm import tqdm
from typing import Tuple

class SimuladorDescarga:
    def __init__(self, tamano_mb: float, velocidad_mbs: float, logger):
        self.tamano_mb = tamano_mb
        self.velocidad_mbs = velocidad_mbs
        self.logger = logger
        self.interrumpido = False
        signal.signal(signal.SIGINT, self._manejar_interrupcion)

    def _manejar_interrupcion(self, sig, frame):
        self.logger.info("Interrupción recibida. Deteniendo simulación...")
        self.interrumpido = True

    def iniciar(self, velocidad_sim: float) -> Tuple[datetime.datetime, datetime.datetime]:
        hora_inicio = datetime.datetime.now()
        tiempo_inicio_simulado = hora_inicio.timestamp()
        tiempo_total_real = self.tamano_mb / self.velocidad_mbs

        self.logger.info(f"Iniciando simulación con velocidad {velocidad_sim}x...")

        # Usamos tqdm para la barra de progreso
        with tqdm(total=self.tamano_mb, unit="MB", desc="Descargando", leave=False) as pbar:
            while self.datos_descargados_mb < self.tamano_mb and not self.interrumpido:
                tiempo_actual_real = datetime.datetime.now().timestamp()
                tiempo_transcurrido_simulado = (tiempo_actual_real - tiempo_inicio_simulado) * velocidad_sim
                self.datos_descargados_mb = min(self.velocidad_mbs * tiempo_transcurrido_simulado, self.tamano_mb)

                pbar.n = self.datos_descargados_mb
                pbar.refresh()

                time.sleep(0.05)

        hora_fin = datetime.datetime.now()
        self.logger.info("Simulación finalizada.")
        return hora_inicio, hora_fin

    @property
    def datos_descargados_mb(self):
        return getattr(self, '_datos_descargados_mb', 0.0)

    @datos_descargados_mb.setter
    def datos_descargados_mb(self, value):
        self._datos_descargados_mb = value