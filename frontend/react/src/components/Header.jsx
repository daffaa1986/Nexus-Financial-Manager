import React, { useRef } from 'react'

export default function Header({ onUpload, loading }) {
  const fileRef = useRef(null)

  const handleClick = () => fileRef.current?.click()
  const handleChange = (e) => {
    const file = e.target.files[0]
    if (file) { onUpload(file); e.target.value = '' }
  }

  return (
    <header className="flex justify-between items-center mb-10">
      <div className="relative w-1/2">
        <span className="absolute inset-y-0 left-4 flex items-center text-gray-400">
          <i className="fas fa-search"></i>
        </span>
        <input type="text" placeholder="Search transactions..."
          className="w-full pl-12 pr-4 py-3 rounded-2xl bg-white border border-transparent focus:border-blue-500 outline-none shadow-sm transition" />
      </div>
      <div className="flex items-center space-x-6">
        <div className="relative inline-block">
          <button onClick={handleClick}
            className={`bg-[#2563EB] text-white px-5 py-2.5 rounded-2xl flex items-center space-x-2 shadow-lg shadow-blue-200 hover:bg-blue-700 transition ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}>
            <i className={`fas ${loading ? 'fa-spinner fa-spin' : 'fa-plus-circle'} text-sm`}></i>
            <span>{loading ? 'Processing...' : 'Upload File'}</span>
          </button>
          <input ref={fileRef} type="file" accept=".pdf,.jpg,.jpeg,.png,.webp"
            onChange={handleChange} className="hidden" />
        </div>
        <div className="relative text-gray-500 cursor-pointer">
          <i className="far fa-bell text-xl"></i>
          <span className="absolute -top-1 -right-0.5 w-2 h-2 bg-red-500 rounded-full"></span>
        </div>
        <div className="flex items-center space-x-3 border-l pl-6 border-gray-200">
          <div className="text-right leading-tight">
            <p className="font-bold text-sm">Architect Prime</p>
            <p className="text-[10px] text-gray-400 uppercase tracking-wider">Pro Account</p>
          </div>
          <img src="https://i.pravatar.cc/150?u=a042581f4e29026704d" alt="Avatar"
            className="w-10 h-10 rounded-full ring-2 ring-blue-100" />
        </div>
      </div>
    </header>
  )
}
