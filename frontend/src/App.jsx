import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = "http://127.0.0.1:8000"
const mapSize = 500;
const scale = 5;

// Estilos
const panelStyle = { border: '1px solid #ddd', padding: '20px', borderRadius: '8px', background: '#f9f9f9', height: '100%', display: 'flex', flexDirection: 'column' }
const statBox = { background: 'white', padding: '15px', borderRadius: '5px', border: '1px solid #eee', marginBottom: '15px' }
const btnStyle = { width: '100%', padding: '10px', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontSize: '14px', fontWeight: 'bold', marginBottom: '5px' }
const tabActive = { padding: '10px 20px', cursor: 'pointer', background: '#333', color: 'white', border: 'none', borderRadius: '5px 5px 0 0', fontWeight: 'bold' }
const tabInactive = { padding: '10px 20px', cursor: 'pointer', background: '#eee', color: '#666', border: 'none', borderRadius: '5px 5px 0 0' }

// Componente ADMIN con botón de Simulación
const VistaAdmin = ({ infoEmpresa, taxis, mejorTaxi, registrarTaxi, eliminarTaxi, simulacionActiva, toggleSimulacion }) => (
  <div style={panelStyle}>
    <h3>👮‍♂️ Panel de Administración</h3>
    
    <div style={statBox}>
      <p>Ganancia Total: <strong>${infoEmpresa.ganancia}</strong></p>
      <p>Viajes Totales: <strong>{infoEmpresa.viajes}</strong></p>
      
      {/* BOTÓN DE SIMULACIÓN AUTOMÁTICA */}
      <div style={{marginTop: 10, paddingTop: 10, borderTop: '1px solid #eee'}}>
        <button 
          onClick={() => toggleSimulacion(!simulacionActiva)}
          style={{...btnStyle, background: simulacionActiva ? '#6f42c1' : '#6c757d'}}
        >
          {simulacionActiva ? '🛑 DETENER SIMULACIÓN' : '🤖 INICIAR SIMULACIÓN AUTO'}
        </button>
        <small style={{color: '#666'}}>
          {simulacionActiva ? "Generando clientes automáticamente..." : "Modo Manual"}
        </small>
      </div>
      
      <hr style={{margin: '10px 0', border: '0', borderTop: '1px solid #eee'}}/>
      
      {mejorTaxi ? (
        <div style={{background: '#fff8e1', padding: '10px', borderRadius: '5px', border: '1px solid #ffe082'}}>
          <span>🏆 <strong>Empleado del Mes:</strong></span><br/>
          #{mejorTaxi.id} ({mejorTaxi.modelo}) - ${mejorTaxi.ganancias}
        </div>
      ) : <p style={{color: '#999', fontStyle: 'italic'}}>Sin datos.</p>}
    </div>

    <button onClick={registrarTaxi} style={{...btnStyle, background: '#007bff'}}>
      ➕ Contratar Nuevo Taxi
    </button>
    
    <h4>Gestión de Flota ({taxis.length})</h4>
    <div style={{flex: 1, overflowY: 'auto', border: '1px solid #eee', background: 'white', padding: '5px', borderRadius: '5px'}}>
      {taxis.length === 0 ? <p style={{fontSize: 12, color: '#999', textAlign: 'center'}}>No hay taxis.</p> : (
        <ul style={{listStyle: 'none', padding: 0, margin: 0}}>
          {taxis.map(t => (
            <li key={t.id} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '5px', borderBottom: '1px solid #f0f0f0', fontSize: '13px'}}>
              <span>
                <strong>#{t.id}</strong> {t.modelo} 
                <span style={{fontSize: 10, marginLeft: 5, color: t.estado==='LIBRE'?'green':'red'}}>({t.estado})</span>
              </span>
              <button 
                onClick={() => eliminarTaxi(t.id)}
                disabled={t.estado === 'OCUPADO'}
                style={{background: t.estado === 'OCUPADO' ? '#ccc' : '#dc3545', color: 'white', border: 'none', borderRadius: '3px', padding: '2px 8px', cursor: 'pointer'}}
              >🗑️</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  </div>
)

const VistaCliente = ({ miIdCliente, setMiIdCliente, solicitarViaje, mensaje }) => (
  <div style={panelStyle}>
    <h3>🙋‍♂️ App de Cliente</h3>
    <div style={{marginBottom: 20}}>
      <label>Tu ID:</label>
      <input type="number" min="1" value={miIdCliente} onChange={(e) => setMiIdCliente(e.target.value)} style={{width: '50px', marginLeft: 10}}/>
    </div>
    <button onClick={solicitarViaje} style={{...btnStyle, background: '#28a745'}}>🚕 Solicitar Viaje</button>
    <div style={{marginTop: 10, padding: 10, background: '#e9ffe9', border: '1px solid #b2d8b2', borderRadius: '5px', fontSize: '13px'}}>
      <strong>Estado:</strong> {mensaje}
    </div>
  </div>
)

const VistaTaxista = ({ taxis, miIdTaxi, setMiIdTaxi }) => {
  const miTaxiDatos = taxis.find(t => t.id === parseInt(miIdTaxi))
  return (
    <div style={panelStyle}>
      <h3>🚖 App de Conductor</h3>
      <div style={{marginBottom: 15}}>
        <label>Soy el Taxi ID: </label>
        <select onChange={(e) => setMiIdTaxi(e.target.value)} value={miIdTaxi || ''}>
          <option value="">Seleccionar...</option>
          {taxis.map(t => <option key={t.id} value={t.id}>#{t.id} - {t.modelo}</option>)}
        </select>
      </div>
      {miTaxiDatos ? (
        <div style={statBox}>
          <p>Estado: <strong style={{color: miTaxiDatos.estado === 'LIBRE' ? 'green' : 'red'}}>{miTaxiDatos.estado}</strong></p>
          <p>Mis Ganancias: <strong>${miTaxiDatos.ganancias.toFixed(2)}</strong></p>
          <p>Placa: <strong>{miTaxiDatos.placa}</strong></p>
          <p>Calif: <strong>⭐ {miTaxiDatos.calificacion}</strong></p>
          {miTaxiDatos.estado === 'OCUPADO' && <div style={{marginTop: 10, padding: 5, background: '#fff3cd', fontSize: 12}}>⚠️ PASAJERO A BORDO</div>}
        </div>
      ) : <p style={{color: '#666'}}>Selecciona tu ID.</p>}
    </div>
  )
}

export default function App() {
  const [taxis, setTaxis] = useState([])
  const [infoEmpresa, setInfoEmpresa] = useState({ ganancia: 0, viajes: 0 })
  const [mejorTaxi, setMejorTaxi] = useState(null)
  const [simulacionActiva, setSimulacionActiva] = useState(false) // Estado simulación
  
  const [rolActual, setRolActual] = useState('ADMIN') 
  const [mensaje, setMensaje] = useState("Sistema iniciado.")
  const [miIdTaxi, setMiIdTaxi] = useState(null)
  const [miIdCliente, setMiIdCliente] = useState(1)

  useEffect(() => {
    const intervalo = setInterval(async () => {
      try {
        const res = await axios.get(`${API_URL}/estado`)
        setTaxis(res.data.taxis)
        setInfoEmpresa({ ganancia: res.data.empresa_ganancia, viajes: res.data.viajes })
        setMejorTaxi(res.data.mejor_taxi)
        setSimulacionActiva(res.data.simulacion_activa)
      } catch (e) { console.error("Conectando...") }
    }, 500)
    return () => clearInterval(intervalo)
  }, [])

  const registrarTaxi = async () => {
    try {
      await axios.post(`${API_URL}/taxis`, { modelo: "Toyota", placa: `ABC-${Math.floor(Math.random() * 999)}` })
      setMensaje("Admin: Taxi creado.")
    } catch (e) { setMensaje("Error al crear taxi.") }
  }

  const eliminarTaxi = async (id) => {
    try {
      await axios.delete(`${API_URL}/taxis/${id}`)
      setMensaje(`Admin: Taxi ${id} eliminado.`)
    } catch (error) { alert("No se pudo eliminar: " + error.response.data.detail) }
  }

  // --- NUEVA FUNCIÓN PARA ACTIVAR SIMULACIÓN ---
  const toggleSimulacion = async (activar) => {
    try {
      await axios.post(`${API_URL}/simulacion/toggle`, { activa: activar })
      setMensaje(activar ? "Simulación INICIADA" : "Simulación DETENIDA")
    } catch (e) { console.error(e) }
  }

  const solicitarViaje = async () => {
    setMensaje("Buscando...")
    try {
      const res = await axios.post(`${API_URL}/solicitar_viaje`, {
        cliente_id: miIdCliente, origen_x: Math.random()*100, origen_y: Math.random()*100, destino_x: Math.random()*100, destino_y: Math.random()*100
      })
      if (res.data.taxi_id) setMensaje(`Asignado Taxi #${res.data.taxi_id}`)
      else setMensaje(res.data.resultado)
    } catch (e) { setMensaje("Error de conexión.") }
  }

  return (
    <div style={{ fontFamily: 'Arial', padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', borderBottom: '2px solid #ccc', paddingBottom: '10px' }}>
        <button onClick={() => setRolActual('ADMIN')} style={rolActual === 'ADMIN' ? tabActive : tabInactive}>👮‍♂️ ADMIN</button>
        <button onClick={() => setRolActual('CLIENTE')} style={rolActual === 'CLIENTE' ? tabActive : tabInactive}>🙋‍♂️ CLIENTE</button>
        <button onClick={() => setRolActual('TAXI')} style={rolActual === 'TAXI' ? tabActive : tabInactive}>🚖 TAXISTA</button>
      </div>

      <div style={{ display: 'flex', gap: '20px', height: '600px' }}>
        <div style={{ width: '350px', height: '100%' }}>
          {rolActual === 'ADMIN' && 
            <VistaAdmin 
              infoEmpresa={infoEmpresa} taxis={taxis} mejorTaxi={mejorTaxi} 
              registrarTaxi={registrarTaxi} eliminarTaxi={eliminarTaxi}
              simulacionActiva={simulacionActiva} toggleSimulacion={toggleSimulacion}
            />
          }
          {rolActual === 'CLIENTE' && <VistaCliente miIdCliente={miIdCliente} setMiIdCliente={setMiIdCliente} solicitarViaje={solicitarViaje} mensaje={mensaje} />}
          {rolActual === 'TAXI' && <VistaTaxista taxis={taxis} miIdTaxi={miIdTaxi} setMiIdTaxi={setMiIdTaxi} />}
          <div style={{marginTop: 10, fontSize: 12, color: '#999'}}>Log: {mensaje}</div>
        </div>

        <div style={{ position: 'relative', width: mapSize, height: mapSize, background: '#eee', border: '3px solid #333' }}>
          <span style={{position:'absolute', top: 5, left: 5, color: '#888', fontWeight: 'bold'}}>MAPA CIUDAD (Simulación)</span>
          {taxis.map(taxi => (
            <div key={taxi.id} style={{
                position: 'absolute', left: taxi.x * scale, top: taxi.y * scale, width: '18px', height: '18px',
                background: taxi.estado === 'LIBRE' ? '#28a745' : '#dc3545', borderRadius: '50%',
                border: miIdTaxi == taxi.id && rolActual === 'TAXI' ? '3px solid blue' : '2px solid white',
                boxShadow: '0 2px 5px rgba(0,0,0,0.3)', transition: 'all 0.5s linear', zIndex: miIdTaxi == taxi.id ? 100 : 1
              }} title={`Taxi ${taxi.id}`}>
              {rolActual === 'TAXI' && miIdTaxi == taxi.id && <span style={{position:'absolute', top:-20, left:-10, background:'blue', color:'white', padding:'2px 5px', borderRadius:4, fontSize:10}}>Yo</span>}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}