// Author: Ronald Wen
import React from 'react'
import ReactDOM from 'react-dom/client'
import axios from 'axios'
import App from './App'
import './index.css'

// In production, point axios at the deployed backend via VITE_API_URL.
// Default '' keeps relative paths so the nginx / Vite dev proxy handles routing locally.
axios.defaults.baseURL = import.meta.env.VITE_API_URL ?? ''

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
