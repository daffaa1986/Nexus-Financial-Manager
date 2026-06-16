import React from 'react'
import { Link } from 'react-router-dom'

const menuItems = [
  { path: '/', icon: 'fa-th-large', label: 'Dashboard' },
  { path: '/time-analysis', icon: 'far fa-clock', label: 'Time Analysis' },
  { path: '/category-manager', icon: 'fa-layer-group', label: 'Category Manager' },
  { path: '/goals-budgeting', icon: 'fa-bullseye', label: 'Goals Budgeting' },
  { path: '/reports-export', icon: 'far fa-chart-bar', label: 'Reports & Export' },
  { path: '/community-insight', icon: 'fa-users', label: 'Community & Insight' },
]

export default function Sidebar({ currentPath }) {
  return (
    <aside className="w-72 bg-[#0F172A] text-white flex flex-col p-6 fixed h-full">
      <div className="mb-10">
        <h1 className="text-2xl font-bold tracking-tight">Nexus Finance</h1>
        <p className="text-[10px] text-gray-400 tracking-[0.2em] uppercase">React Edition</p>
      </div>
      <nav className="flex-1 space-y-2 text-gray-400">
        {menuItems.map(item => (
          <Link key={item.path} to={item.path}
            className={`flex items-center space-x-3 p-3 rounded-xl transition ${
              currentPath === item.path ? 'bg-[#1E3A8A]/30 text-blue-400' : 'hover:bg-slate-800'
            }`}>
            <i className={`${item.icon} w-5 text-center`}></i>
            <span className="font-medium">{item.label}</span>
          </Link>
        ))}
      </nav>
      <div className="mt-auto space-y-2 text-gray-400 pt-6 border-t border-slate-800">
        <Link to="/settings" className="flex items-center space-x-3 p-3 hover:text-white transition">
          <i className="fas fa-cog"></i><span>Settings</span>
        </Link>
        <Link to="/profile" className="flex items-center space-x-3 p-3 hover:text-white transition">
          <i className="far fa-user"></i><span>Profile</span>
        </Link>
        <Link to="/login" className="flex items-center space-x-3 p-3 hover:text-white transition mt-4">
          <i className="fas fa-sign-out-alt"></i><span>Logout</span>
        </Link>
      </div>
    </aside>
  )
}
