import threading
import math
import random
from datetime import datetime, timedelta
from .taxi import Taxi
from .cliente import Cliente

class SistemaUnieTaxi:
    def __init__(self):
        self.taxis = []     
        self.clientes = []  
        self.cola_espera = []
        
        self.ganancia_empresa = 0.0
        self.viajes_totales = 0
        self.contador_id_taxi = 0 
        self.contador_id_cliente = 0
        self.clientes_viajando = set() 

        self.ultimo_refuerzo = datetime.min
        self.tiempo_actual = datetime(2025, 12, 12, 6, 0, 0) 

        self.mutex_taxis = threading.RLock() 
        self.mutex_contabilidad = threading.RLock()

    def tick_tiempo(self):
        self.tiempo_actual += timedelta(minutes=20)

    # --- DESPACHADOR CENTRAL ---
    def procesar_despacho_automatico(self):
        """Asigna taxis libres a clientes en espera."""
        with self.mutex_taxis:
            # Si no hay nadie esperando o no hay taxis, salimos rápido
            if not self.cola_espera: return

            # Buscamos LIBRES
            taxis_libres = [t for t in self.taxis if t.estado == "LIBRE"]
            
            # Asignamos en bucle hasta que se acaben los taxis o la cola
            while taxis_libres and self.cola_espera:
                taxi = taxis_libres.pop(0)
                exito = self.asignar_trabajo_de_cola(taxi)
                if exito:
                    print(f"[DESPACHO] 🔗 Taxi {taxi.id} emparejado con cola.")

    # --- GERENTE (CON DIAGNÓSTICO) ---
    def gestionar_abastecimiento(self):
        LIMITE_FLOTA = 50  # <--- SUBIDO A 50
        TIEMPO_ENTRE_CONTRATACIONES = 0.5 
        ahora_real = datetime.now() 

        with self.mutex_taxis:
            cola_len = len(self.cola_espera)
            
            # Solo actuamos si hay "presión" (cola >= 5)
            if cola_len < 5: return

            # 1. CHECK LÍMITE
            if len(self.taxis) >= LIMITE_FLOTA:
                # Opcional: Descomenta para ver si llegaste al tope
                # print(f"[GERENCIA] ⛔ No se contrata: Límite de flota alcanzado ({len(self.taxis)}/{LIMITE_FLOTA})")
                return 

            # 2. CHECK TIEMPO
            segundos_pasados = (ahora_real - self.ultimo_refuerzo).total_seconds()
            if segundos_pasados < TIEMPO_ENTRE_CONTRATACIONES:
                return 

            # 3. CONTRATACIÓN
            print(f"[GERENCIA] ⚡ Contratando refuerzo por cola de {cola_len} pax.")
            self.registrar_taxi("Refuerzo-Flash", f"R-{random.randint(100,999)}")
            self.ultimo_refuerzo = ahora_real

    def registrar_taxi(self, modelo, placa):
        self.contador_id_taxi += 1
        nuevo_taxi = Taxi(self.contador_id_taxi, modelo, placa, float(random.uniform(0, 100)), float(random.uniform(0, 100)))
        with self.mutex_taxis:
            self.taxis.append(nuevo_taxi)
            # Intenta coger trabajo nada más nacer
            self.asignar_trabajo_de_cola(nuevo_taxi)
        return nuevo_taxi

    def registrar_cliente(self, nombre, tarjeta):
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
            # Prioridad: Atender cola primero si existe (para mantener orden FIFO)
            # Pero para simplificar, buscamos libre directo.
            for taxi in self.taxis:
                if taxi.estado == "LIBRE":
                    dist = math.sqrt((taxi.x - float(ox))**2 + (taxi.y - float(oy))**2)
                    if dist < distancia_minima:
                        distancia_minima = dist
                        mejor_taxi = taxi
            
            if mejor_taxi:
                self._asignar_viaje(mejor_taxi, cliente_id, ox, oy, dx, dy)
                return mejor_taxi
            else:
                solicitud = {"cliente_id": cliente_id, "ox": ox, "oy": oy, "dx": dx, "dy": dy}
                self.cola_espera.append(solicitud)
                self.clientes_viajando.add(cliente_id)
                return "EN_COLA"

    def _asignar_viaje(self, taxi, cliente_id, ox, oy, dx, dy):
        taxi.estado = "OCUPADO"
        taxi.destino_actual = (float(dx), float(dy))
        taxi.x = float(ox) 
        taxi.y = float(oy)
        taxi.cliente_actual = cliente_id 
        self.clientes_viajando.add(cliente_id)

    def asignar_trabajo_de_cola(self, taxi):
        # Esta función asume que ya estamos dentro de un lock (with self.mutex_taxis)
        if self.cola_espera:
            siguiente = self.cola_espera.pop(0) 
            self._asignar_viaje(
                taxi, siguiente["cliente_id"], 
                siguiente["ox"], siguiente["oy"], 
                siguiente["dx"], siguiente["dy"]
            )
            return True
        return False

    def finalizar_viaje(self, taxi, costo):
        if taxi.cliente_actual:
            cliente_obj = next((c for c in self.clientes if c.id == taxi.cliente_actual), None)
            if cliente_obj: cliente_obj.viajes += 1 
            if taxi.cliente_actual in self.clientes_viajando:
                self.clientes_viajando.remove(taxi.cliente_actual)
            taxi.cliente_actual = None

        with self.mutex_contabilidad:
            comision = costo * 0.20
            pago_taxi = costo - comision
            taxi.ganancias += pago_taxi
            taxi.viajes += 1 
            self.ganancia_empresa += comision
            self.viajes_totales += 1

    def eliminar_taxi(self, taxi_id):
        with self.mutex_taxis:
            taxi_a_borrar = next((t for t in self.taxis if t.id == taxi_id), None)
            if not taxi_a_borrar: return False, "Taxi no encontrado"
            if taxi_a_borrar.estado == "OCUPADO": return False, "No se puede eliminar: Ocupado."
            self.taxis.remove(taxi_a_borrar)
            return True, "Taxi eliminado."