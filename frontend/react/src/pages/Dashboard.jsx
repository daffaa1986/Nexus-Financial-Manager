import React, { useContext, useEffect, useRef } from 'react'
import { Chart, registerables } from 'chart.js'
import { AppContext } from '../App'

Chart.register(...registerables)

export default function Dashboard() {
  const { transactions, insights } = useContext(AppContext)
  const radarRef = useRef(null)
  const chartRef = useRef(null)

  const totalIncome = transactions.filter(t => t.type === 'CR').reduce((s, t) => s + t.amount, 0)
  const totalExpense = transactions.filter(t => t.type === 'DB').reduce((s, t) => s + t.amount, 0)
  const balance = totalIncome - totalExpense

  const categorySums = {}
  transactions.filter(t => t.type === 'DB').forEach(t => {
    const cat = t.category || 'Lainnya'
    categorySums[cat] = (categorySums[cat] || 0) + t.amount
  })

  useEffect(() => {
    if (!radarRef.current) return
    if (chartRef.current) chartRef.current.destroy()

    const labels = Object.keys(categorySums).length ? Object.keys(categorySums) : ['Menunggu Data']
    const data = Object.keys(categorySums).length ? Object.values(categorySums) : [0]

    chartRef.current = new Chart(radarRef.current, {
      type: 'radar',
      data: {
        labels,
        datasets: [{
          label: 'Pengeluaran (Rp)',
          data,
          backgroundColor: 'rgba(37, 99, 235, 0.2)',
          borderColor: '#2563EB',
          borderWidth: 2,
          pointBackgroundColor: '#2563EB',
          pointRadius: 4
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          r: {
            angleLines: { color: '#f1f5f9' }, grid: { color: '#f1f5f9' },
            pointLabels: { font: { size: 10 }, color: '#45464D' },
            ticks: { display: false }
          }
        }
      }
    })
    return () => { if (chartRef.current) chartRef.current.destroy() }
  }, [transactions])

  return (
    <>
      <section className="mb-10">
        <h2 className="text-[11px] text-gray-400 uppercase tracking-[0.2em] font-bold mb-1">Consolidated Overview</h2>
        <div className="flex items-baseline space-x-3">
          <h3 className="text-5xl font-black tracking-tight">
            Rp {balance.toLocaleString('id-ID')}
            <span className="text-2xl text-gray-400 font-medium">.00</span>
          </h3>
        </div>
      </section>

      <div className="grid grid-cols-4 gap-6 mb-10">
        {[
          { label: 'Total Income', value: totalIncome, color: 'green', icon: 'fa-arrow-trend-up' },
          { label: 'Expenses', value: totalExpense, color: 'red', icon: 'fa-arrow-trend-down' },
          { label: 'Savings', value: totalIncome - totalExpense, color: 'blue', icon: 'fa-wallet' },
          { label: 'Transactions', value: transactions.length, color: 'indigo', icon: 'fa-chart-pie' },
        ].map(card => (
          <div key={card.label} className={`bg-white p-6 rounded-[2rem] shadow-sm border border-gray-50`}>
            <div className={`w-10 h-10 rounded-xl bg-${card.color}-50 flex items-center justify-center mb-6`}>
              <i className={`fas ${card.icon} text-${card.color === 'red' ? '[#BA1A1A]' : card.color === 'green' ? '[#009668]' : card.color === 'blue' ? '[#2563EB]' : '[#497CFF]'}`}></i>
            </div>
            <p className="text-[10px] uppercase tracking-widest text-gray-400 font-bold mb-1">{card.label}</p>
            <h4 className="text-3xl font-black">Rp {card.value.toLocaleString('id-ID')}</h4>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-12 gap-8 mb-10">
        <div className="col-span-7 bg-white p-8 rounded-[2rem] shadow-sm border border-gray-50">
          <h3 className="text-xl font-black mb-6">Expense Architecture</h3>
          <div className="aspect-square max-w-xs mx-auto">
            <canvas ref={radarRef}></canvas>
          </div>
        </div>
        <div className="col-span-5 bg-white p-8 rounded-[2rem] shadow-sm border border-gray-50">
          <h3 className="text-xl font-black mb-4">AI Spending Insights</h3>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {!insights ? (
              <div className="p-6 text-center text-gray-400">
                <i className="fas fa-robot text-3xl mb-3 text-blue-400"></i>
                <p className="font-bold">AI sedang menganalisis...</p>
                <p className="text-xs mt-1">Upload mutasi untuk melihat insight.</p>
              </div>
            ) : insights.insights?.length > 0 ? (
              insights.insights.map((item, i) => (
                <div key={i} className={`p-4 rounded-xl border-l-4 mb-3 ${
                  item.type === 'bocor' ? 'bg-red-50 border-red-500' :
                  item.type === 'boros' ? 'bg-orange-50 border-orange-500' :
                  'bg-blue-50 border-blue-500'
                }`}>
                  <div className="flex items-start space-x-3">
                    <i className={`fas ${
                      item.type === 'bocor' ? 'fa-exclamation-triangle text-red-500' :
                      item.type === 'boros' ? 'fa-fire text-orange-500' :
                      'fa-lightbulb text-blue-500'
                    } mt-1`}></i>
                    <div>
                      <h4 className="font-bold text-sm">{item.title}</h4>
                      <p className="text-xs text-gray-600">{item.description}</p>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="p-6 text-center text-green-500">
                <i className="fas fa-check-circle text-3xl mb-3"></i>
                <p className="font-bold">Keuangan Anda dalam kondisi baik!</p>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="bg-white p-8 rounded-[2rem] shadow-sm border border-gray-50">
        <h3 className="text-xl font-black mb-6">Monthly Ledger</h3>
        <table className="w-full text-left">
          <thead>
            <tr className="text-[10px] uppercase text-gray-400 font-bold border-b border-gray-100">
              <th className="pb-3 px-2">Date</th>
              <th className="pb-3 px-2">Label</th>
              <th className="pb-3 px-2">Category</th>
              <th className="pb-3 px-2 text-right">Amount</th>
              <th className="pb-3 px-2 text-right">Source</th>
            </tr>
          </thead>
          <tbody>
            {transactions.slice(0, 10).map((t, i) => (
              <tr key={i} className="border-b border-gray-50 hover:bg-slate-50 transition">
                <td className="py-4 px-2 font-bold">{t.date}</td>
                <td className="py-4 px-2 text-gray-800 font-bold">{t.label}</td>
                <td className="py-4 px-2 text-gray-500">{t.category}</td>
                <td className={`py-4 px-2 font-bold text-right ${t.type === 'DB' ? 'text-red-500' : 'text-green-500'}`}>
                  {t.type === 'DB' ? '-' : '+'}Rp {t.amount.toLocaleString('id-ID')}
                </td>
                <td className="py-4 px-2 text-right">
                  <span className={`text-[9px] px-2 py-1 rounded-md uppercase font-black shadow-sm ${
                    t.source === 'mutation' ? 'bg-blue-50 text-blue-600' :
                    t.source === 'receipt' ? 'bg-purple-50 text-purple-600' :
                    'bg-blue-50 text-blue-600'
                  }`}>
                    {t.source === 'receipt' ? 'OCR Struk' : 'AI Mutasi'}
                  </span>
                </td>
              </tr>
            ))}
            {transactions.length === 0 && (
              <tr><td colSpan="5" className="py-8 text-center text-gray-400">Belum ada transaksi. Upload file untuk memulai.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  )
}
