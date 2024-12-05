import random

def seleccionar_premio(premios):
    """
    Selecciona un premio basado en probabilidades.
    
    :param premios: Lista de diccionarios con clave 'nombre' y 'probabilidad'.
    :return: Nombre del premio seleccionado o "Gracias por participar".
    """
    # Crear una lista de probabilidades acumulativas
    total = sum(p['probabilidad'] for p in premios)
    if total == 0:
        return "Gracias por participar"  # Evitar división por cero
    
    # Normalizar probabilidades si no suman exactamente 100
    acumulativo = 0
    probabilidades = []
    for premio in premios:
        acumulativo += premio['probabilidad'] / total
        probabilidades.append((acumulativo, premio['nombre']))
    
    # Generar un número aleatorio entre 0 y 1
    aleatorio = random.random()
    
    # Determinar el premio correspondiente
    for prob, nombre in probabilidades:
        if aleatorio <= prob:
            return nombre
    
    return "Gracias por participar"
