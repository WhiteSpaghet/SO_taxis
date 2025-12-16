import math
import random

class Taxi:
    def __init__(self, id, modelo, placa, x, y):
        self.id = id
        self.modelo = modelo
        self.placa = placa
        # Aseguramos float desde el nacimiento
        self.x = float(x)
        self.y = float(y)
        self.estado = "LIBRE"
        self.calificacion = round(random.uniform(3.5, 5.0), 2)
        self.ganancias = 0.0
        self.destino_actual = None
        self.cliente_actual = None

    def actualizar_posicion(self, destino_x, destino_y, velocidad):
        try:
            # 1. FORZAMOS DATOS A DECIMALES (Crucial)
            origen_x = float(self.x)
            origen_y = float(self.y)
            dest_x = float(destino_x)
            dest_y = float(destino_y)
            vel = float(velocidad)

            # 2. CALCULO VECTORIAL
            diff_x = dest_x - origen_x
            diff_y = dest_y - origen_y
            
            # Pitágoras
            distancia = math.sqrt(diff_x**2 + diff_y**2)

            # DEBUG: Si quieres ver las tripas, descomenta esto:
            # print(f"Taxi {self.id}: Distancia {distancia:.2f} - Vel {vel}")

            # 3. CASO: YA LLEGAMOS (O estamos muy cerca)
            if distancia < 1.0: 
                self.x = dest_x
                self.y = dest_y
                return True # LLEGADA CONFIRMADA

            # 4. CASO: SALTO FINAL (Para no pasarse)
            if distancia <= vel:
                self.x = dest_x
                self.y = dest_y
                return True # LLEGADA CONFIRMADA

            # 5. MOVIMIENTO NORMAL
            # Normalizamos el vector (lo hacemos de tamaño 1) y multiplicamos por velocidad
            factor = vel / distancia
            
            self.x += diff_x * factor
            self.y += diff_y * factor

            return False # AUN EN CAMINO

        except Exception as e:
            print(f"[ERROR MATH TAXI {self.id}]: {e}")
            # Si falla las mates, teletransportamos para desatascar
            self.x = destino_x
            self.y = destino_y
            return True