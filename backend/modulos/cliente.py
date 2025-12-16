class Cliente:
    def __init__(self, id, nombre, tarjeta_credito):
        self.id = id
        self.nombre = nombre
        self.tarjeta_credito = tarjeta_credito
        self.viajes = 0 # <--- NUEVO CONTADOR
        self.posicion_x = 0.0
        self.posicion_y = 0.0
        
    # Nota: No necesitamos mucha lógica aquí, el sistema lo gestiona todo.

    def solicitar_viaje(self, origen_x, origen_y, destino_x, destino_y):
        """Registra la intención de viaje del cliente."""
        self.posicion_x = origen_x
        self.posicion_y = origen_y
        # Aquí se podrían añadir lógicas futuras como validar saldo
        return {
            "cliente_id": self.id,
            "origen": (origen_x, origen_y),
            "destino": (destino_x, destino_y)
        }