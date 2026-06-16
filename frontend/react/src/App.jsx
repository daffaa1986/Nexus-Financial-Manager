import React, { useState, useEffect } from 'react'
import { Routes, Route, useLocation } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './pages/Dashboard'

const API_BASE = '/api'

export const AppContext = React.createContext()

export default function App() {
  const [transactions, setTransactions] = useState([])
  const [insights, setInsights] = useState(null)
  const [loading, setLoading] = useState(false)
  const location = useLocation()

  const fetchTransactions = async () => {
    try {
      const res = await fetch(`${API_BASE}/transactions`)
      const data = await res.json()
      if (data.status === 'success') setTransactions(data.data)
    } catch (e) {
      console.error('Gagal ambil transaksi:', e)
    }
  }

  const fetchInsights = async () => {
    try {
      const now = new Date()
      const res = await fetch(`${API_BASE}/insights?bulan=${now.getMonth()+1}&tahun=${now.getFullYear()}`)
      const data = await res.json()
      if (data.status === 'success') setInsights(data.data)
    } catch (e) {
      console.error('Gagal ambil insights:', e)
    }
  }

  const handleUpload = async (file) => {
    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)
    try {
      await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData })
      setTimeout(() => {
        fetchTransactions()
        fetchInsights()
        setLoading(false)
      }, 3000)
    } catch (e) {
      alert('Upload gagal!')
      setLoading(false)
    }
  }

  useEffect(() => { fetchTransactions(); fetchInsights() }, [])

  return (
    <AppContext.Provider value={{ transactions, insights, loading, fetchTransactions, fetchInsights, handleUpload }}>
      <div className="flex min-h-screen bg-[#FAF8FF] font-['Plus_Jakarta_Sans']">
        <Sidebar currentPath={location.pathname} />
        <main className="flex-1 ml-72 p-8 overflow-y-auto">
          <Header onUpload={handleUpload} loading={loading} />
          <Routes>
            <Route path="/" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </AppContext.Provider>
  )
}
