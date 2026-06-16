<template>
  <div class="flex min-h-screen bg-[#FAF8FF]" style="font-family: 'Plus Jakarta Sans', sans-serif;">
    <aside class="w-72 bg-[#0F172A] text-white flex flex-col p-6 fixed h-full">
      <div class="mb-10">
        <h1 class="text-2xl font-bold tracking-tight">Nexus Finance</h1>
        <p class="text-[10px] text-gray-400 tracking-[0.2em] uppercase">Vue Edition</p>
      </div>
      <nav class="flex-1 space-y-2 text-gray-400">
        <router-link v-for="item in menuItems" :key="item.path" :to="item.path"
          class="flex items-center space-x-3 p-3 rounded-xl transition"
          :class="$route.path === item.path ? 'bg-[#1E3A8A]/30 text-blue-400' : 'hover:bg-slate-800'">
          <i :class="item.icon" class="w-5 text-center"></i>
          <span class="font-medium">{{ item.label }}</span>
        </router-link>
      </nav>
      <div class="mt-auto space-y-2 text-gray-400 pt-6 border-t border-slate-800">
        <router-link to="/settings" class="flex items-center space-x-3 p-3 hover:text-white transition">
          <i class="fas fa-cog"></i><span>Settings</span>
        </router-link>
        <router-link to="/profile" class="flex items-center space-x-3 p-3 hover:text-white transition">
          <i class="far fa-user"></i><span>Profile</span>
        </router-link>
        <router-link to="/login" class="flex items-center space-x-3 p-3 hover:text-white transition mt-4">
          <i class="fas fa-sign-out-alt"></i><span>Logout</span>
        </router-link>
      </div>
    </aside>
    <main class="flex-1 ml-72 p-8 overflow-y-auto">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      menuItems: [
        { path: '/', icon: 'fas fa-th-large', label: 'Dashboard' },
        { path: '/time-analysis', icon: 'far fa-clock', label: 'Time Analysis' },
        { path: '/category-manager', icon: 'fas fa-layer-group', label: 'Category Manager' },
        { path: '/goals-budgeting', icon: 'fas fa-bullseye', label: 'Goals Budgeting' },
        { path: '/reports-export', icon: 'far fa-chart-bar', label: 'Reports & Export' },
        { path: '/community-insight', icon: 'fas fa-users', label: 'Community & Insight' },
      ]
    }
  }
}
</script>
