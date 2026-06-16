<template>
  <div>
    <!-- Header -->
    <header class="flex justify-between items-center mb-10">
      <div class="relative w-1/2">
        <span class="absolute inset-y-0 left-4 flex items-center text-gray-400">
          <i class="fas fa-search"></i>
        </span>
        <input type="text" placeholder="Search transactions..."
          class="w-full pl-12 pr-4 py-3 rounded-2xl bg-white border border-transparent focus:border-blue-500 outline-none shadow-sm transition" />
      </div>
      <div class="flex items-center space-x-6">
        <div class="relative inline-block">
          <button @click="triggerUpload" :disabled="loading"
            class="bg-[#2563EB] text-white px-5 py-2.5 rounded-2xl flex items-center space-x-2 shadow-lg shadow-blue-200 hover:bg-blue-700 transition"
            :class="{ 'opacity-70 cursor-not-allowed': loading }">
            <i :class="`fas text-sm ${loading ? 'fa-spinner fa-spin' : 'fa-plus-circle'}`"></i>
            <span>{{ loading ? 'Processing...' : 'Upload File' }}</span>
          </button>
          <input ref="fileInput" type="file" accept=".pdf,.jpg,.jpeg,.png,.webp" @change="handleUpload" class="hidden" />
        </div>
        <div class="relative text-gray-500 cursor-pointer">
          <i class="far fa-bell text-xl"></i>
          <span class="absolute -top-1 -right-0.5 w-2 h-2 bg-red-500 rounded-full"></span>
        </div>
        <div class="flex items-center space-x-3 border-l pl-6 border-gray-200">
          <div class="text-right leading-tight">
            <p class="font-bold text-sm">Architect Prime</p>
            <p class="text-[10px] text-gray-400 uppercase tracking-wider">Pro Account</p>
          </div>
          <img src="https://i.pravatar.cc/150?u=a042581f4e29026704d" alt="Avatar"
            class="w-10 h-10 rounded-full ring-2 ring-blue-100" />
        </div>
      </div>
    </header>

    <!-- Stats -->
    <section class="mb-10">
      <h2 class="text-[11px] text-gray-400 uppercase tracking-[0.2em] font-bold mb-1">Consolidated Overview</h2>
      <div class="flex items-baseline space-x-3">
        <h3 class="text-5xl font-black tracking-tight">
          Rp {{ formatNumber(balance) }}<span class="text-2xl text-gray-400 font-medium">.00</span>
        </h3>
      </div>
    </section>

    <div class="grid grid-cols-4 gap-6 mb-10">
      <div v-for="card in statCards" :key="card.label" class="bg-white p-6 rounded-[2rem] shadow-sm border border-gray-50">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center mb-6" :style="{ backgroundColor: card.bg }">
          <i :class="`fas ${card.icon}`" :style="{ color: card.color }"></i>
        </div>
        <p class="text-[10px] uppercase tracking-widest text-gray-400 font-bold mb-1">{{ card.label }}</p>
        <h4 class="text-3xl font-black">Rp {{ formatNumber(card.value) }}</h4>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-12 gap-8 mb-10">
      <div class="col-span-7 bg-white p-8 rounded-[2rem] shadow-sm border border-gray-50">
        <h3 class="text-xl font-black mb-6">Expense Architecture</h3>
        <div class="aspect-square max-w-xs mx-auto">
          <canvas ref="radarCanvas"></canvas>
        </div>
      </div>
      <div class="col-span-5 bg-white p-8 rounded-[2rem] shadow-sm border border-gray-50">
        <h3 class="text-xl font-black mb-4">AI Spending Insights</h3>
        <div class="space-y-3 max-h-96 overflow-y-auto">
          <div v-if="!insights" class="p-6 text-center text-gray-400">
            <i class="fas fa-robot text-3xl mb-3 text-blue-400"></i>
            <p class="font-bold">AI sedang menganalisis...</p>
          </div>
          <div v-else-if="insights.insights?.length" v-for="(item, i) in insights.insights" :key="i"
            class="p-4 rounded-xl border-l-4 mb-3"
            :class="insightClass(item.type)">
            <div class="flex items-start space-x-3">
              <i :class="`fas mt-1 ${insightIcon(item.type)}`"></i>
              <div>
                <h4 class="font-bold text-sm">{{ item.title }}</h4>
                <p class="text-xs text-gray-600">{{ item.description }}</p>
              </div>
            </div>
          </div>
          <div v-else class="p-6 text-center text-green-500">
            <i class="fas fa-check-circle text-3xl mb-3"></i>
            <p class="font-bold">Keuangan Anda dalam kondisi baik!</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Ledger Table -->
    <div class="bg-white p-8 rounded-[2rem] shadow-sm border border-gray-50">
      <h3 class="text-xl font-black mb-6">Monthly Ledger</h3>
      <table class="w-full text-left">
        <thead>
          <tr class="text-[10px] uppercase text-gray-400 font-bold border-b border-gray-100">
            <th class="pb-3 px-2">Date</th>
            <th class="pb-3 px-2">Label</th>
            <th class="pb-3 px-2">Category</th>
            <th class="pb-3 px-2 text-right">Amount</th>
            <th class="pb-3 px-2 text-right">Source</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(t, i) in transactions.slice(0, 10)" :key="i"
            class="border-b border-gray-50 hover:bg-slate-50 transition">
            <td class="py-4 px-2 font-bold">{{ t.date }}</td>
            <td class="py-4 px-2 text-gray-800 font-bold">{{ t.label }}</td>
            <td class="py-4 px-2 text-gray-500">{{ t.category }}</td>
            <td class="py-4 px-2 font-bold text-right" :class="t.type === 'DB' ? 'text-red-500' : 'text-green-500'">
              {{ t.type === 'DB' ? '-' : '+' }}Rp {{ formatNumber(t.amount) }}
            </td>
            <td class="py-4 px-2 text-right">
              <span class="text-[9px] px-2 py-1 rounded-md uppercase font-black shadow-sm"
                :class="t.source === 'receipt' ? 'bg-purple-50 text-purple-600' : 'bg-blue-50 text-blue-600'">
                {{ t.source === 'receipt' ? 'OCR Struk' : 'AI Mutasi' }}
              </span>
            </td>
          </tr>
          <tr v-if="!transactions.length">
            <td colspan="5" class="py-8 text-center text-gray-400">Belum ada transaksi.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

const API_BASE = '/api'

export default {
  data() {
    return {
      transactions: [],
      insights: null,
      loading: false,
      chartInstance: null,
    }
  },
  computed: {
    totalIncome() { return this.transactions.filter(t => t.type === 'CR').reduce((s, t) => s + t.amount, 0) },
    totalExpense() { return this.transactions.filter(t => t.type === 'DB').reduce((s, t) => s + t.amount, 0) },
    balance() { return this.totalIncome - this.totalExpense },
    statCards() {
      return [
        { label: 'Total Income', value: this.totalIncome, icon: 'fa-arrow-trend-up', bg: '#ECFDF5', color: '#009668' },
        { label: 'Expenses', value: this.totalExpense, icon: 'fa-arrow-trend-down', bg: '#FEF2F2', color: '#BA1A1A' },
        { label: 'Savings', value: this.balance, icon: 'fa-wallet', bg: '#EFF6FF', color: '#2563EB' },
        { label: 'Transactions', value: this.transactions.length, icon: 'fa-chart-pie', bg: '#EEF2FF', color: '#497CFF' },
      ]
    },
    categorySums() {
      const sums = {}
      this.transactions.filter(t => t.type === 'DB').forEach(t => {
        const cat = t.category || 'Lainnya'
        sums[cat] = (sums[cat] || 0) + t.amount
      })
      return sums
    }
  },
  methods: {
    formatNumber(n) { return Number(n || 0).toLocaleString('id-ID') },
    insightClass(type) {
      return {
        bocor: 'bg-red-50 border-red-500',
        boros: 'bg-orange-50 border-orange-500',
        tip: 'bg-blue-50 border-blue-500',
        good: 'bg-green-50 border-green-500'
      }[type] || 'bg-blue-50 border-blue-500'
    },
    insightIcon(type) {
      return {
        bocor: 'fa-exclamation-triangle text-red-500',
        boros: 'fa-fire text-orange-500',
        tip: 'fa-lightbulb text-blue-500',
        good: 'fa-check-circle text-green-500'
      }[type] || 'fa-lightbulb text-blue-500'
    },
    triggerUpload() { this.$refs.fileInput?.click() },
    async handleUpload(e) {
      const file = e.target.files[0]
      if (!file) return
      this.loading = true
      const fd = new FormData()
      fd.append('file', file)
      try {
        await fetch(`${API_BASE}/upload`, { method: 'POST', body: fd })
        setTimeout(() => { this.fetchData(); this.loading = false }, 3000)
      } catch { alert('Upload gagal!'); this.loading = false }
      e.target.value = ''
    },
    async fetchData() {
      try {
        const [txRes, inRes] = await Promise.all([
          fetch(`${API_BASE}/transactions`),
          fetch(`${API_BASE}/insights?bulan=${new Date().getMonth()+1}&tahun=${new Date().getFullYear()}`)
        ])
        const tx = await txRes.json()
        const ins = await inRes.json()
        if (tx.status === 'success') this.transactions = tx.data
        if (ins.status === 'success') this.insights = ins.data
      } catch (e) { console.error(e) }
    },
    initRadar() {
      if (this.chartInstance) this.chartInstance.destroy()
      const labels = Object.keys(this.categorySums).length ? Object.keys(this.categorySums) : ['Menunggu Data']
      const data = Object.keys(this.categorySums).length ? Object.values(this.categorySums) : [0]
      this.chartInstance = new Chart(this.$refs.radarCanvas, {
        type: 'radar',
        data: {
          labels,
          datasets: [{
            label: 'Pengeluaran (Rp)', data,
            backgroundColor: 'rgba(37, 99, 235, 0.2)',
            borderColor: '#2563EB', borderWidth: 2,
            pointBackgroundColor: '#2563EB', pointRadius: 4
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
    }
  },
  mounted() { this.fetchData() },
  watch: {
    categorySums: { deep: true, handler() { this.$nextTick(() => this.initRadar()) } }
  },
  beforeUnmount() { if (this.chartInstance) this.chartInstance.destroy() }
}
</script>
