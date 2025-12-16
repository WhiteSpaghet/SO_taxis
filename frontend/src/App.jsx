import { useState, useEffect } from 'react'
import axios from 'axios'

/* No importamos CSS aquí para evitar errores */

function App() {
  const [tareas, setTareas] = useState([])
  const [nuevoTitulo, setNuevoTitulo] = useState("")
  const API_URL = "http://127.0.0.1:8000"

  const cargarTareas = async () => {
    try {
      const respuesta = await axios.get(`${API_URL}/tareas`)
      setTareas(respuesta.data)
    } catch (error) {
      console.error("Error cargando tareas:", error)
    }
  }

  const manejarEnvio = async (e) => {
    e.preventDefault()
    if (!nuevoTitulo) return
    try {
      await axios.post(`${API_URL}/tareas`, {
        titulo: nuevoTitulo,
        completada: false
      })
      setNuevoTitulo("")
      cargarTareas()
    } catch (error) {
      console.error("Error:", error)
    }
  }

  useEffect(() => {
    cargarTareas()
  }, [])

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Gestor de Tareas</h1>
      <form onSubmit={manejarEnvio} style={{ marginBottom: '20px' }}>
        <input 
          value={nuevoTitulo}
          onChange={(e) => setNuevoTitulo(e.target.value)}
          placeholder="Nueva tarea..."
        />
        <button type="submit">Agregar</button>
      </form>
      <ul>
        {tareas.map((t) => (
          <li key={t.id}>{t.titulo}</li>
        ))}
      </ul>
    </div>
  )
}

export default App