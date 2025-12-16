import threading
import math
import random
from .taxi import Taxi
from .cliente import Cliente

class SistemaUnieTaxi:
    def __init__(self):
        self.taxis = []     # Lista de objetos Taxi
        self.clientes = []  # Lista de objetos Cliente
        self.ganancia_empresa = 0.0
        self.viajes_totales = 0
        
        # --- CONTROL DE ESTADO DE PROCESOS (NUEVO) ---
        # Este conjunto (Set) almacena los IDs de los clientes que están ocupados.
        # Funciona como un bloqueo lógico para el usuario.
        self.clientes_viajando = set() 

        # --- RECURSOS CRÍTICOS Y SINCRONIZACIÓN ---
        self.mutex_taxis = threading.Lock()
        self.mutex_contabilidad = threading.Lock()

    def registrar_taxi(self, modelo, placa):
        # Simulamos verificación de antecedentes (10% fallo)
        if random.random() < 0.1: return None
        
        nuevo_taxi = Taxi(
            id=len(self.taxis) + 1,
            modelo=modelo,
            placa=placa,
            x=random.uniform(0, 100),
            y=random.uniform(0, 100)
        )
        with self.mutex_taxis:
            self.taxis.append(nuevo_taxi)
        return nuevo_taxi

    def registrar_cliente(self, nombre, tarjeta):
        nuevo_cliente = Cliente(len(self.clientes)+1, nombre, tarjeta)
        self.clientes.append(nuevo_cliente)
        return nuevo_cliente

    def procesar_solicitud(self, cliente_id, ox, oy, dx, dy):
        """Algoritmo de Match Cliente-Taxi con Validaciones"""
        
        # 1. VALIDACIÓN DE ID NEGATIVO
        if cliente_id <= 0:
            return "ID_INVALIDO"

        # 2. VALIDACIÓN DE ESTADO (Usuario ya viaja)
        if cliente_id in self.clientes_viajando:
            return "CLIENTE_OCUPADO" 

        mejor_taxi = None
        distancia_minima = float('inf')

        # 3. SECCIÓN CRÍTICA (Buscar taxi)
        with self.mutex_taxis:
            for taxi in self.taxis:
                if taxi.estado == "LIBRE":
                    dist = math.sqrt((taxi.x - ox)**2 + (taxi.y - oy)**2)
                    
                    if dist <= 20: 
                        if dist < distancia_minima:
                            distancia_minima = dist
                            mejor_taxi = taxi
                        elif dist == distancia_minima:
                            if taxi.calificacion > mejor_taxi.calificacion:
                                mejor_taxi = taxi
            
            # 4. ASIGNACIÓN
            if mejor_taxi:
                mejor_taxi.estado = "OCUPADO"
                mejor_taxi.destino_actual = (dx, dy)
                mejor_taxi.x = ox
                mejor_taxi.y = oy
                mejor_taxi.cliente_actual = cliente_id 
                
                # Bloqueamos al cliente
                self.clientes_viajando.add(cliente_id)
            else:
                return "SIN_TAXIS" # Devolvemos código específico si no hay coches
        
        return mejor_taxi

    def finalizar_viaje(self, taxi, costo):
        """Cierre contable y liberación de recursos"""
        
        # 1. LIBERACIÓN DEL PROCESO CLIENTE
        # Si el taxi traía un cliente, lo desbloqueamos
        if taxi.cliente_actual in self.clientes_viajando:
            self.clientes_viajando.remove(taxi.cliente_actual)
            taxi.cliente_actual = None # Limpiamos el taxi

        # 2. SECCIÓN CRÍTICA CONTABLE
        with self.mutex_contabilidad:
            comision = costo * 0.20
            pago_taxi = costo - comision
            
            taxi.ganancias += pago_taxi
            self.ganancia_empresa += comision
            self.viajes_totales += 1
            
            # Auditoría aleatoria (1 de cada 5 viajes)
            if self.viajes_totales % 5 == 0:
                print(f"[AUDITORÍA CALIDAD] Revisando viaje del Taxi {taxi.placa}...")