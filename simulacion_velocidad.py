# Simulación de tiempos de viaje
def calcular_tiempo(distancia, velocidad):
    tiempo_horas = distancia / velocidad
    horas = int(tiempo_horas)
    minutos = int((tiempo_horas - horas) * 60)
    return horas, minutos

# Datos
distancia_total = 100  # km
distancia_david = 100 # km (desde su posición actual)
vel_javier = 50  # km/h
vel_david = 50   # km/h

# Cálculos
t_javier_h, t_javier_m = calcular_tiempo(distancia_total, vel_javier)
t_david_h, t_david_m = calcular_tiempo(distancia_david, vel_david)

print(f"Javier (carro): {t_javier_h} horas y {t_javier_m} minutos")
print(f"David (bicicleta): {t_david_h} horas y {t_david_m} minutos")