import threading
import time
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Importamos nuestros MÓDULOS PROPIOS
from modulos.sistema import SistemaUnieTaxi

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instanciamos el sistema central
sistema = SistemaUnieTaxi()

# --- HILO DE SIMULACIÓN (MOTOR FÍSICO) ---
# Esto cumple el requisito de "hilos que simulan entidades ejecutándose concurrentemente"
def motor_fisica():
    while True:
        # Accedemos a la lista de taxis de forma segura
        with sistema.mutex_taxis:
            for taxi in sistema.taxis:
                if taxi.estado == "OCUPADO" and taxi.destino_actual:
                    dest_x, dest_y = taxi.destino_actual
                    
                    # Usamos el método del módulo Taxi
                    llegado = taxi.actualizar_posicion(dest_x, dest_y)
                    
                    if llegado:
                        taxi.estado = "LIBRE"
                        taxi.destino_actual = None
                        costo_viaje = random.uniform(10, 50)
                        sistema.finalizar_viaje(taxi, costo_viaje)
        
        time.sleep(0.5)

hilo_motor = threading.Thread(target=motor_fisica, daemon=True)
hilo_motor.start()

# --- DTOs (Data Transfer Objects) para la API ---
class TaxiRegistro(BaseModel):
    modelo: str
    placa: str

class SolicitudViaje(BaseModel):
    cliente_id: int
    origen_x: float
    origen_y: float
    destino_x: float
    destino_y: float

# --- RUTAS DE LA API ---

@app.get("/estado")
def ver_estado():
    # Calculamos el taxi con más ganancias al vuelo
    mejor_taxi = None
    if sistema.taxis:
        # Buscamos el objeto taxi con el atributo 'ganancias' más alto
        mejor_taxi_obj = max(sistema.taxis, key=lambda t: t.ganancias)
        if mejor_taxi_obj.ganancias > 0:
            mejor_taxi = {
                "id": mejor_taxi_obj.id, 
                "modelo": mejor_taxi_obj.modelo, 
                "ganancias": round(mejor_taxi_obj.ganancias, 2)
            }

    return {
        "taxis": sistema.taxis,
        "empresa_ganancia": round(sistema.ganancia_empresa, 2),
        "viajes": sistema.viajes_totales,
        "mejor_taxi": mejor_taxi  # <--- NUEVO CAMPO
    }

@app.delete("/taxis/{taxi_id}")
def borrar_taxi(taxi_id: int):
    exito, mensaje = sistema.eliminar_taxi(taxi_id)
    if not exito:
        raise HTTPException(status_code=400, detail=mensaje)
    return {"mensaje": mensaje}

@app.post("/taxis")
def crear_taxi(datos: TaxiRegistro):
    taxi = sistema.registrar_taxi(datos.modelo, datos.placa)
    if not taxi:
        raise HTTPException(status_code=400, detail="Rechazado por antecedentes")
    return taxi

@app.post("/solicitar_viaje")
def solicitar(datos: SolicitudViaje):
    resultado = sistema.procesar_solicitud(
        datos.cliente_id, 
        datos.origen_x, datos.origen_y, 
        datos.destino_x, datos.destino_y
    )
    
    # Manejo de Errores Específicos
    if resultado == "ID_INVALIDO":
        return {"resultado": "Error: El ID debe ser positivo."}
    
    if resultado == "CLIENTE_OCUPADO":
        return {"resultado": f"Error: El usuario {datos.cliente_id} ya tiene un viaje."}
        
    if resultado == "SIN_TAXIS":
        return {"resultado": "No hay taxis disponibles cerca (2km)."}
    
    # Si llegamos aquí, es que 'resultado' es un objeto Taxi válido
    return {
        "resultado": "Taxi asignado",
        "taxi_id": resultado.id,
        "modelo": resultado.modelo
    }