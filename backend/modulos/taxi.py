import random

class Taxi:
    def __init__(self, id, modelo, placa, x, y):
        self.id = id
        self.modelo = modelo
        self.placa = placa
        self.x = x
        self.y = y
        self.estado = "LIBRE"
        self.calificacion = round(random.uniform(3.5, 5.0), 2)
        self.ganancias = 0.0
        self.destino_actual = None
        self.cliente_actual = None

    def actualizar_posicion(self, destino_x, destino_y, velocidad=2):
        """
        Mueve el taxi hacia el destino.
        Retorna True si ha llegado, False si sigue viajando.
        """
        dx = destino_x - self.x
        dy = destino_y - self.y
        distancia = (dx**2 + dy**2)**0.5
        
        # 1. Si ya estamos ahí (o muy cerca), terminamos.
        if distancia < 0.1:
            self.x = destino_x
            self.y = destino_y
            return True

        # 2. Si la distancia es menor que la velocidad, damos un "salto final"
        # para evitar pasarnos y vibrar (Overshooting).
        if distancia <= velocidad:
            self.x = destino_x
            self.y = destino_y
            return True
        
        # 3. Movimiento normal
        self.x += (dx / distancia) * velocidad
        self.y += (dy / distancia) * velocidad
        return False