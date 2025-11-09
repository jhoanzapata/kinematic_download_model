import datetime
import json
import os

def guardar_reporte(hora_inicio: datetime.datetime, hora_fin: datetime.datetime, tiempo_teorico_segundos: float):
    minutos_teoricos = int(tiempo_teorico_segundos // 60)
    segundos_teoricos = int(tiempo_teorico_segundos % 60)
    tiempo_teorico_str = f"{minutos_teoricos} minutos y {segundos_teoricos} segundos"

    reporte = {
        "hora_inicio": hora_inicio.isoformat(),
        "hora_fin": hora_fin.isoformat(),
        "duracion_simulacion": str(hora_fin - hora_inicio),
        "tiempo_teorico_real": tiempo_teorico_str
    }

    # Guardar como JSON
    with open("reporte_simulacion.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=4, ensure_ascii=False)

    # Guardar como TXT
    with open("reporte_simulacion.txt", "w", encoding="utf-8") as f:
        f.write("--- Reporte de Simulación ---\n")
        f.write(f"Hora de inicio:       {hora_inicio.strftime('%H:%M:%S')}\n")
        f.write(f"Hora de finalización: {hora_fin.strftime('%H:%M:%S')}\n")
        f.write(f"Duración de la simulación: {hora_fin - hora_inicio}\n")
        f.write(f"Tiempo teórico real:   {tiempo_teorico_str}\n")
        f.write("------------------------------------\n")

    print("\n✅ Reporte guardado en 'reporte_simulacion.json' y 'reporte_simulacion.txt'.")