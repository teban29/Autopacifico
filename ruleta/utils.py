import random

def seleccionar_premio(premios):
    """
    Selecciona un premio basado en probabilidades.
    - premios: lista de diccionarios con 'nombre', 'probabilidad' y 'estado'.
    Retorna el nombre del premio o "Sin premio".
    """
    opciones = []
    for premio in premios:
        if premio['estado']:  # Solo considerar premios activos
            opciones.append((premio['nombre'], premio['probabilidad']))
    # Añadir casillas "Sin premio"
    opciones.append(("Sin premio", 80))  # 80% de probabilidad
    total = sum(p[1] for p in opciones)  # Sumar todas las probabilidades

    # Generar un número aleatorio y seleccionar premio
    numero = random.uniform(0, total)
    acumulado = 0
    for opcion, probabilidad in opciones:
        acumulado += probabilidad
        if numero <= acumulado:
            return opcion
    return "Sin premio"

