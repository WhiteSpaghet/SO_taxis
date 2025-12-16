import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'  /* <--- ASEGÚRATE DE QUE ESTA LÍNEA ESTÉ */

/* No debe haber imports de CSS aquí si no tienes los archivos */

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)