import threading
import math
import random
from .taxi import Taxi
from .cliente import Cliente

class SistemaUnieTaxi:
    def __init__(self):
        self.taxis = []     
        self.clientes = []  
        self.ganancia_empresa = 0.0
        self.viajes_totales = 0
        
        # CONTADORES PERSISTENTES (IDs únicos)
        self.contador_id_taxi = 0 
        self.contador_id_cliente = 0 # <--- NUEVO
        
        self.clientes_viajando = set() 
        self.mutex_taxis = threading.Lock()
        self.mutex_contabilidad = threading.Lock()

    def registrar_taxi(self, modelo, placa):
        if random.random() < 0.1: return None
        self.contador_id_taxi += 1
        nuevo_taxi = Taxi(self.contador_id_taxi, modelo, placa, random.uniform(0, 100), random.uniform(0, 100))
        with self.mutex_taxis:
            self.taxis.append(nuevo_taxi)
        return nuevo_taxi

    def registrar_cliente(self, nombre, tarjeta):
        # Generamos ID único para clientes también
        self.contador_id_cliente += 1
        nuevo_cliente = Cliente(self.contador_id_cliente, nombre, tarjeta)
        self.clientes.append(nuevo_cliente)
        return nuevo_cliente

    def procesar_solicitud(self, cliente_id, ox, oy, dx, dy):
        if cliente_id <= 0: return "ID_INVALIDO"
        if cliente_id in self.clientes_viajando: return "CLIENTE_OCUPADO" 

        mejor_taxi = None
        distancia_minima = float('inf')

        with self.mutex_taxis:
            for taxi in self.taxis:
                if taxi.estado == "LIBRE":
                    dist = math.sqrt((taxi.x - ox)**2 + (taxi.y - oy)**2)
                    
                    # --- CAMBIO AQUÍ: YA NO HAY LÍMITE DE DISTANCIA ---
                    # Antes: if dist <= 20: ...
                    # Ahora: Siempre buscamos el menor, esté donde esté.
                    
                    if dist < distancia_minima:
                        distancia_minima = dist
                        mejor_taxi = taxi
                    elif dist == distancia_minima:
                        if taxi.calificacion > mejor_taxi.calificacion:
                            mejor_taxi = taxi
            
            if mejor_taxi:
                mejor_taxi.estado = "OCUPADO"
                mejor_taxi.destino_actual = (dx, dy)
                mejor_taxi.x = ox
                mejor_taxi.y = oy
                mejor_taxi.cliente_actual = cliente_id 
                self.clientes_viajando.add(cliente_id)
            else:
                return "SIN_TAXIS"
        
        return mejor_taxi

    def finalizar_viaje(self, taxi, costo):
        if taxi.cliente_actual in self.clientes_viajando:
            self.clientes_viajando.remove(taxi.cliente_actual)
            taxi.cliente_actual = None

        with self.mutex_contabilidad:
            comision = costo * 0.20
            pago_taxi = costo - comision
            taxi.ganancias += pago_taxi
            self.ganancia_empresa += comision
            self.viajes_totales += 1

    def eliminar_taxi(self, taxi_id):
        with self.mutex_taxis:
            taxi_a_borrar = next((t for t in self.taxis if t.id == taxi_id), None)
            if not taxi_a_borrar: return False, "Taxi no encontrado"
            if taxi_a_borrar.estado == "OCUPADO": return False, "No se puede eliminar: Ocupado."
            self.taxis.remove(taxi_a_borrar)
            return True, "Taxi eliminado."