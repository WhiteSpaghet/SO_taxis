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
        self.destino_actual = None
        self.cliente_actual = None

    def actualizar_posicion(self, destino_x, destino_y, velocidad=2):
        try:
            # 1. Protección contra datos corruptos (NaN)
            if math.isnan(self.x) or math.isnan(self.y):
                self.x = float(destino_x)
                self.y = float(destino_y)
                return True

            dx = float(destino_x) - self.x
            dy = float(destino_y) - self.y
            distancia = math.sqrt(dx**2 + dy**2)
            
            # 2. Si ya estamos ahí, terminar.
            if distancia < 0.5: # Margen de error un poco más grande
                self.x = destino_x
                self.y = destino_y
                return True

            # 3. Lógica de "salto" si estamos cerca (Anti-vibración)
            if distancia <= velocidad:
                self.x = destino_x
                self.y = destino_y
                return True
            
            # 4. Movimiento normal
            factor = velocidad / distancia
            self.x += dx * factor
            self.y += dy * factor
            return False

        except Exception as e:
            print(f"[ERROR MATH TAXI {self.id}]: {e}")
            return True # Ante la duda, llegamos al destino