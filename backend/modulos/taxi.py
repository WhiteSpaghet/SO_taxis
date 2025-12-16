import random

class Taxi:
    def __init__(self, id, modelo, placa, x, y):
        self.id = id
        self.modelo = modelo
        self.placa = placa
        self.x = x
        self.y = y
        self.estado = "LIBRE"  # Estados: LIBRE, OCUPADO
        self.calificacion = round(random.uniform(3.5, 5.0), 2)
        self.ganancias = 0.0
        self.destino_actual = None
        self.cliente_actual = None

    def actualizar_posicion(self, destino_x, destino_y, velocidad=2):
        """Simula el movimiento del taxi hacia un destino."""
        dx = destino_x - self.x
        dy = destino_y - self.y
        distancia = (dx**2 + dy**2)**0.5
        
        if distancia < 1:
            self.x = destino_x
            self.y = destino_y
            return True # Ha llegado
        else:
            # Avanzar un paso hacia el destino
            self.x += (dx / distancia) * velocidad
            self.y += (dy / distancia) * velocidad
            return False # Sigue en camino