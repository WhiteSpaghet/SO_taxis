import math
import random

class Taxi:
    def __init__(self, id, modelo, placa, x, y):
        self.id = id
        self.modelo = modelo
        self.placa = placa
        self.x = float(x)
        self.y = float(y)
        self.estado = "LIBRE"
        self.calificacion = round(random.uniform(3.5, 5.0), 2)
        self.ganancias = 0.0
        self.viajes = 0  # <--- NUEVO CONTADOR
        self.destino_actual = None
        self.cliente_actual = None

    def actualizar_posicion(self, destino_x, destino_y, velocidad):
        # 1. Calculamos la distancia total al objetivo
        dx = float(destino_x) - self.x
        dy = float(destino_y) - self.y
        distancia = math.sqrt(dx**2 + dy**2)
        
        # 2. Si ya estamos prácticamente encima, retornamos True
        if distancia < 0.1:
            self.x = destino_x
            self.y = destino_y
            return True

        # "Si la velocidad es mayor a la distancia, 
        # cambiamos la velocidad a la necesaria para recorrer esa distancia"
        velocidad_turno = velocidad
        
        if velocidad > distancia:
            velocidad_turno = distancia # Frenado exacto

        # 3. Aplicamos el movimiento con la nueva velocidad ajustada
        if distancia > 0:
            ratio = velocidad_turno / distancia
            self.x += dx * ratio
            self.y += dy * ratio

        # 4. Comprobamos si hemos terminado
        if distancia <= velocidad:
            return True
            
        return False