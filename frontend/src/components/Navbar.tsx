// Author: Ronald Wen
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { setToken } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    setToken(null)
    navigate('/login')
  }

  return (
    <nav className="bg-navy-800 border-b border-slate-700 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <span className="text-xl font-bold text-white tracking-tight">FraudGuard</span>
        <button
          onClick={handleLogout}
          className="text-sm text-slate-400 hover:text-white border border-slate-600 hover:border-slate-400 px-4 py-1.5 rounded-lg transition"
        >
          Logout
        </button>
      </div>
    </nav>
  )
}
