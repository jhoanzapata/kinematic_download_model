import datetime
import time
from simulator import SimuladorDescarga
from logger import setup_logger
from reporter import guardar_reporte

# --- CONFIGURACIÓN GLOBAL ---
VELOCIDAD_SIMULACION = 100.0


def obtener_datos_usuario():
    """Solicita al usuario la velocidad y el tamaño del archivo."""
    print("--- Simulador de Descargas: Modelo Cinemático (v3 Profesional) ---")
    try:
        velocidad_mbps = float(input("Ingresa la velocidad de tu internet (en Mbps): "))
        tamano_gb = float(input("Ingresa el tamaño del archivo a descargar (en GB): "))
        if velocidad_mbps <= 0 or tamano_gb <= 0:
            raise ValueError("Los valores deben ser positivos.")
        return velocidad_mbps, tamano_gb
    except ValueError as e:
        print(f"Error: {e}. Por favor, ingresa solo números válidos y positivos.")
        return None, None


def calcular_parametros_fisicos(velocidad_mbps: float, tamano_gb: float):
    """Convierte y calcula los parámetros necesarios para la simulación."""
    velocidad_mbs = velocidad_mbps / 8.0
    tamano_mb = tamano_gb * 1024.0
    tiempo_total_segundos = tamano_mb / velocidad_mbs
    return velocidad_mbs, tamano_mb, tiempo_total_segundos


def main():
    logger = setup_logger()
    velocidad, tamano = obtener_datos_usuario()

    if velocidad is not None and tamano is not None:
        vel_mbs, total_mb, tiempo_seg = calcular_parametros_fisicos(velocidad, tamano)

        logger.info(f"Simulación iniciada con {vel_mbs:.2f} MB/s y {total_mb:.2f} MB.")

        simulador = SimuladorDescarga(total_mb, vel_mbs, logger)
        inicio, fin = simulador.iniciar(VELOCIDAD_SIMULACION)

        if not simulador.interrumpido:
            logger.info("Simulación completada exitosamente.")
            mostrar_reporte_final(inicio, fin, tiempo_seg)
            guardar_reporte(inicio, fin, tiempo_seg)
        else:
            logger.warning("Simulación interrumpida por el usuario.")


def mostrar_reporte_final(hora_inicio: datetime.datetime, hora_fin: datetime.datetime, tiempo_teorico_segundos: float):
    """Muestra un reporte final en consola."""
    print("\n--- Reporte Final de la Descarga ---")
    print(f"Hora de inicio:       {hora_inicio.strftime('%H:%M:%S')}")
    print(f"Hora de finalización: {hora_fin.strftime('%H:%M:%S')}")
    print(f"Duración de la simulación: {hora_fin - hora_inicio}")

    minutos_teoricos = int(tiempo_teorico_segundos // 60)
    segundos_teoricos = int(tiempo_teorico_segundos % 60)
    print(f"Tiempo teórico real:   {minutos_teoricos} minutos y {segundos_teoricos} segundos")
    print("------------------------------------")


if __name__ == "__main__":
    main()