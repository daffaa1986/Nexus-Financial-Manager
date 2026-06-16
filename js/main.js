const API_BASE = "http://127.0.0.1:8000";

document.addEventListener('DOMContentLoaded', function () {
    let expenseRadarChart;
    let expenseBarChart;
    let trendLineChart;

    const radarElement = document.getElementById('radarChart');
    if (radarElement) {
        const radarCtx = radarElement.getContext('2d');
        expenseRadarChart = new Chart(radarCtx, {
            type: 'radar',
            data: {
                labels: ['Menunggu Data...'],
                datasets: [{
                    label: 'Pengeluaran (Rp)',
                    data: [0],
                    backgroundColor: 'rgba(37, 99, 235, 0.2)',
                    borderColor: '#2563EB',
                    borderWidth: 2,
                    pointBackgroundColor: '#2563EB',
                    pointBorderColor: '#fff',
                    pointRadius: 4
                }]
            },
            options: {
                plugins: { legend: { display: false } },
                scales: {
                    r: {
                        angleLines: { display: true, color: '#f1f5f9' },
                        grid: { color: '#f1f5f9' },
                        pointLabels: { font: { size: 10, weight: 'bold', family: 'Plus Jakarta Sans' }, color: '#45464D' },
                        ticks: { display: false }
                    }
                }
            }
        });
    }

    const balanceElement = document.getElementById('balanceChart');
    if (balanceElement) {
        const balanceCtx = balanceElement.getContext('2d');
        new Chart(balanceCtx, {
            type: 'bar',
            data: {
                labels: ['AUG 24', 'NOV 24', 'FEB 25', 'MAY 25', 'JUL 25'],
                datasets: [
                    {
                        type: 'line',
                        label: 'Trend',
                        data: [15, 12, 18, 25, 30],
                        borderColor: '#497CFF',
                        borderWidth: 3,
                        fill: false,
                        tension: 0.4,
                        pointRadius: 0
                    },
                    {
                        label: 'Balance',
                        data: [10, 15, 20, 25, 30],
                        backgroundColor: (context) => {
                            const chart = context.chart;
                            const {ctx, chartArea} = chart;
                            if (!chartArea) return null;
                            const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                            gradient.addColorStop(0, '#DBEAFE');
                            gradient.addColorStop(1, '#1E40AF');
                            return gradient;
                        },
                        borderRadius: 8,
                        barThickness: 15
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { display: false, beginAtZero: true },
                    x: {
                        grid: { display: false },
                        border: { display: false },
                        ticks: { color: '#94A3B8', font: { size: 9, weight: 'bold' } }
                    }
                }
            }
        });
    }

    const timeElement = document.getElementById('timeBarChart');
    if (timeElement) {
        const ctx = timeElement.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'],
                datasets: [{
                    label: 'Process Time (ms)',
                    data: [120, 190, 150, 250, 180, 210, 320, 240, 170, 200],
                    backgroundColor: '#DAE2FD',
                    hoverBackgroundColor: '#497CFF',
                    borderRadius: 10,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(200, 200, 200, 0.1)' }, border: { display: false } },
                    x: { grid: { display: false }, border: { display: false } }
                }
            }
        });
    }

    // CATEGORY MANAGER
    const cards = document.querySelectorAll('.category-card');
    const inputName = document.getElementById('input-name');
    const inputBudget = document.getElementById('input-budget');
    const previewTitle = document.getElementById('preview-title');
    const colorOptions = document.querySelectorAll('.color-option');
    const iconOptions = document.querySelectorAll('.icon-option');

    function updateSelectionColors(color) {
        const previewIcon = document.querySelector('.preview-icon');
        if (!previewIcon) return;
        const colorMap = { blue: '#EFF6FF', red: '#FEF2F2', green: '#ECFDF5', purple: '#FAF5FF', orange: '#FFF7ED' };
        const textMap = { blue: '#2563EB', red: '#B91C1C', green: '#047857', purple: '#7C3AED', orange: '#EA580C' };
        previewIcon.style.backgroundColor = colorMap[color] || '#EFF6FF';
        previewIcon.style.color = textMap[color] || '#2563EB';
    }

    function updateFormSelection(color, iconHref) {
        colorOptions.forEach(opt => opt.classList.toggle('selected', opt.classList.contains(color)));
        iconOptions.forEach(opt => {
            const icon = opt.querySelector('svg use');
            opt.classList.toggle('selected', icon && icon.getAttribute('href') === iconHref);
        });
    }

    function setActiveCard(card) {
        cards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        const name = card.dataset.name;
        const limit = card.dataset.limit;
        const color = card.dataset.color;
        const iconElement = card.querySelector('.icon-box svg use');
        const iconHref = iconElement ? iconElement.getAttribute('href') : '';
        if(inputName) inputName.value = name;
        if(previewTitle) previewTitle.innerText = name;
        if(inputBudget) inputBudget.value = parseFloat(limit).toLocaleString('en-US', { minimumFractionDigits: 2 });
        const previewIconElement = document.querySelector('.preview-icon svg use');
        if(previewIconElement && iconHref) previewIconElement.setAttribute('href', iconHref);
        updateSelectionColors(color);
        updateFormSelection(color, iconHref);
    }

    if (cards.length > 0) {
        cards.forEach(card => card.addEventListener('click', () => setActiveCard(card)));
        const activeCard = document.querySelector('.category-card.active');
        if (activeCard) setActiveCard(activeCard);
    }

    if (inputName) inputName.addEventListener('input', (e) => {
        if(previewTitle) previewTitle.innerText = e.target.value;
        const activeCardTitle = document.querySelector('.category-card.active h4');
        if (activeCardTitle) activeCardTitle.innerText = e.target.value;
    });

    if (inputBudget) inputBudget.addEventListener('blur', (e) => {
        const value = e.target.value.replace(/[^0-9.]/g, '');
        if (!value) return;
        e.target.value = parseFloat(value).toLocaleString('en-US', { minimumFractionDigits: 2 });
    });

    if (colorOptions.length > 0) {
        colorOptions.forEach(opt => {
            opt.addEventListener('click', () => {
                colorOptions.forEach(o => o.classList.remove('selected'));
                opt.classList.add('selected');
                const colorKey = Array.from(opt.classList).find(c => ['blue','green','orange','purple','red'].includes(c));
                if (colorKey) updateSelectionColors(colorKey);
            });
        });
    }

    if (iconOptions.length > 0) {
        iconOptions.forEach(opt => {
            opt.addEventListener('click', () => {
                iconOptions.forEach(o => o.classList.remove('selected'));
                opt.classList.add('selected');
                const newIcon = opt.querySelector('svg use');
                const newIconHref = newIcon ? newIcon.getAttribute('href') : '';
                const previewIcon = document.querySelector('.preview-icon svg use');
                if(previewIcon && newIconHref) previewIcon.setAttribute('href', newIconHref);
            });
        });
    }

    // SETTINGS
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) target.scrollIntoView({ behavior: 'smooth' });
        });
    });

    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    const sections = document.querySelectorAll('main section');
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= (sectionTop - sectionHeight / 3)) current = section.getAttribute('id');
        });
        navLinks.forEach(link => {
            link.classList.remove('bg-[#EEF2FF]', 'text-[#2563EB]', 'font-bold', 'bg-red-50');
            if (link.getAttribute('href') !== '#critical') link.classList.add('text-gray-500');
            else link.classList.add('text-[#BA1A1A]');
            if (link.getAttribute('href') === `#${current}`) {
                if (current === 'critical') link.classList.add('bg-red-50', 'font-bold');
                else { link.classList.remove('text-gray-500'); link.classList.add('bg-[#EEF2FF]', 'text-[#2563EB]', 'font-bold'); }
            }
        });
    }, { passive: true });

    // ==========================================
    // AI INSIGHTS DISPLAY
    // ==========================================
    function createInsightCard(insight) {
        const colors = {
            bocor: { bg: 'bg-red-50', border: 'border-red-200', icon: 'fas fa-exclamation-triangle', iconColor: 'text-red-500', badge: 'bg-red-100 text-red-700' },
            boros: { bg: 'bg-orange-50', border: 'border-orange-200', icon: 'fas fa-fire', iconColor: 'text-orange-500', badge: 'bg-orange-100 text-orange-700' },
            tip: { bg: 'bg-blue-50', border: 'border-blue-200', icon: 'fas fa-lightbulb', iconColor: 'text-blue-500', badge: 'bg-blue-100 text-blue-700' },
            good: { bg: 'bg-green-50', border: 'border-green-200', icon: 'fas fa-check-circle', iconColor: 'text-green-500', badge: 'bg-green-100 text-green-700' },
        };
        const sevColors = { high: 'border-l-red-500', medium: 'border-l-yellow-500', low: 'border-l-green-500' };
        const c = colors[insight.type] || colors.tip;
        const sev = sevColors[insight.severity] || 'border-l-gray-300';

        return `
            <div class="p-4 ${c.bg} border ${c.border} border-l-4 ${sev} rounded-xl mb-3">
                <div class="flex items-start space-x-3">
                    <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${c.bg}">
                        <i class="${c.icon} ${c.iconColor} text-sm"></i>
                    </div>
                    <div class="flex-1">
                        <div class="flex items-center space-x-2 mb-1">
                            <h4 class="font-bold text-sm">${insight.title}</h4>
                            <span class="text-[9px] px-2 py-0.5 rounded-full font-bold ${c.badge}">${insight.type.toUpperCase()}</span>
                        </div>
                        <p class="text-xs text-gray-600">${insight.description}</p>
                        ${insight.amount ? `<p class="text-xs font-bold text-gray-700 mt-1">Rp ${insight.amount.toLocaleString('id-ID')}</p>` : ''}
                    </div>
                </div>
            </div>
        `;
    }

    async function muatAIInsights() {
        const container = document.getElementById('aiInsightsContainer');
        if (!container) return;

        try {
            const now = new Date();
            const bulan = now.getMonth() + 1;
            const tahun = now.getFullYear();
            const response = await fetch(`${API_BASE}/api/insights?bulan=${bulan}&tahun=${tahun}`);
            const result = await response.json();

            if (result.status === 'success' && result.data) {
                const data = result.data;

                if (data.summary) {
                    const summaryEl = document.getElementById('aiSummaryText');
                    if (summaryEl) summaryEl.innerHTML = data.summary.replace(/\n/g, '<br>');
                }

                if (data.insights && data.insights.length > 0) {
                    container.innerHTML = data.insights.map(createInsightCard).join('');
                } else {
                    container.innerHTML = `
                        <div class="p-6 text-center text-gray-400">
                            <i class="fas fa-check-circle text-3xl mb-3 text-green-400"></i>
                            <p class="font-bold text-green-600">Keuangan Anda dalam kondisi baik!</p>
                            <p class="text-xs mt-1">Upload mutasi untuk analisis lebih lanjut.</p>
                        </div>
                    `;
                }
            }
        } catch (error) {
            console.error("Gagal memuat AI insights:", error);
        }
    }

    // ==========================================
    // LOAD TRANSACTIONS & UPDATE DASHBOARD
    // ==========================================
    async function muatDataDariDatabase() {
        try {
            const response = await fetch(`${API_BASE}/api/transactions`);
            const result = await response.json();

            if (result.status === "success" && result.data.length > 0) {
                let totalIncome = 0;
                let totalExpense = 0;
                let categorySums = {};

                const tableBody = document.querySelector('table tbody');
                if (tableBody) tableBody.innerHTML = '';

                result.data.forEach(trx => {
                    let type = trx.type;
                    if (!type) type = trx.category === 'Income' ? 'CR' : 'DB';

                    if (type === 'CR') totalIncome += trx.amount;
                    else if (type === 'DB') {
                        totalExpense += trx.amount;
                        let cat = trx.category || "Lainnya";
                        if (cat !== 'Income') categorySums[cat] = (categorySums[cat] || 0) + trx.amount;
                    }

                    if (tableBody) {
                        const newRow = document.createElement('tr');
                        newRow.className = "border-b border-gray-50 group hover:bg-slate-50 transition";
                        const formattedAmount = "Rp " + parseFloat(trx.amount).toLocaleString('id-ID');
                        const isExpense = type === 'DB';
                        const colorClass = isExpense ? 'text-red-500' : 'text-green-500';
                        const sign = isExpense ? '-' : '+';
                        const sourceBadge = trx.source === 'mutation'
                            ? '<span class="bg-blue-50 text-blue-600 text-[9px] px-2 py-1 rounded-md uppercase font-black shadow-sm">AI Mutasi</span>'
                            : '<span class="bg-purple-50 text-purple-600 text-[9px] px-2 py-1 rounded-md uppercase font-black shadow-sm">OCR Struk</span>';

                        newRow.innerHTML = `
                            <td class="py-4 px-2 font-bold">${trx.date}</td>
                            <td class="py-4 px-2 text-gray-800 font-bold">${trx.label}</td>
                            <td class="py-4 px-2 text-gray-500">${trx.category}</td>
                            <td class="py-4 px-2 font-bold text-right ${colorClass}">${sign}${formattedAmount}</td>
                            <td class="py-4 px-2 text-right">${sourceBadge}</td>
                        `;
                        tableBody.appendChild(newRow);
                    }
                });

                const incomeBox = document.querySelector('.bg-green-50')?.parentElement?.querySelector('h4');
                const expenseBox = document.querySelector('.bg-red-50')?.parentElement?.querySelector('h4');
                const mainBalanceBox = document.querySelector('h3.text-5xl.font-black');

                if (incomeBox) incomeBox.innerHTML = `Rp ${totalIncome.toLocaleString('id-ID')}`;
                if (expenseBox) expenseBox.innerHTML = `Rp ${totalExpense.toLocaleString('id-ID')}`;

                let sisaSaldo = totalIncome - totalExpense;
                if (mainBalanceBox) {
                    mainBalanceBox.innerHTML = `Rp ${sisaSaldo.toLocaleString('id-ID')} <span class="text-2xl text-gray-400 font-medium">.00</span>`;
                }

                if (expenseRadarChart && Object.keys(categorySums).length > 0) {
                    expenseRadarChart.data.labels = Object.keys(categorySums);
                    expenseRadarChart.data.datasets[0].data = Object.values(categorySums);
                    expenseRadarChart.update();
                }
            }
        } catch (error) {
            console.error("Belum bisa mengambil data:", error);
        }
    }

    muatDataDariDatabase();
    muatAIInsights();


    // ==========================================
    // EDIT PROFILE
    // ==========================================
    const editProfileBtn = document.getElementById('editProfileBtn');
    if (editProfileBtn) {
        const profileInputs = document.querySelectorAll('#fullName, #emailAddress, #phoneNumber, #architectBio');
        const profileSelects = document.querySelectorAll('#timezone');
        profileInputs.forEach(input => {
            input.setAttribute('readonly', 'true');
            if(input.classList) { input.classList.add('bg-slate-50', 'text-slate-500', 'cursor-not-allowed'); input.classList.remove('bg-white'); }
        });
        profileSelects.forEach(select => {
            select.setAttribute('disabled', 'true');
            if(select.classList) { select.classList.add('bg-slate-50', 'text-slate-500', 'cursor-not-allowed'); select.classList.remove('bg-white'); }
        });

        let isEditing = false;
        editProfileBtn.addEventListener('click', () => {
            isEditing = !isEditing;
            if (isEditing) {
                editProfileBtn.innerHTML = '<i class="fas fa-save mr-2"></i>Save Profile';
                editProfileBtn.classList.replace('bg-[#EEF2FF]', 'bg-[#2563EB]');
                editProfileBtn.classList.replace('text-[#2563EB]', 'text-white');
                profileInputs.forEach(input => { input.removeAttribute('readonly'); input.classList.remove('bg-slate-50', 'text-slate-500', 'cursor-not-allowed'); input.classList.add('bg-white', 'ring-2', 'ring-blue-100'); });
                profileSelects.forEach(select => { select.removeAttribute('disabled'); select.classList.remove('bg-slate-50', 'text-slate-500', 'cursor-not-allowed'); select.classList.add('bg-white', 'ring-2', 'ring-blue-100'); });
            } else {
                editProfileBtn.innerHTML = 'Edit Profile';
                editProfileBtn.classList.replace('bg-[#2563EB]', 'bg-[#EEF2FF]');
                editProfileBtn.classList.replace('text-white', 'text-[#2563EB]');
                profileInputs.forEach(input => { input.setAttribute('readonly', 'true'); input.classList.add('bg-slate-50', 'text-slate-500', 'cursor-not-allowed'); input.classList.remove('bg-white', 'ring-2', 'ring-blue-100'); });
                profileSelects.forEach(select => { select.setAttribute('disabled', 'true'); select.classList.add('bg-slate-50', 'text-slate-500', 'cursor-not-allowed'); select.classList.remove('bg-white', 'ring-2', 'ring-blue-100'); });
            }
        });
    }

    // ==========================================
    // DARK MODE
    // ==========================================
    const darkModeToggles = document.querySelectorAll('.dark-mode-toggle');
    const isDarkMode = localStorage.getItem('darkMode') === 'true';

    function updateSettingsUI(isDark) {
        const btnLight = document.getElementById('btnLightMode');
        const btnDark = document.getElementById('btnDarkMode');
        if (btnLight && btnDark) {
            if (isDark) {
                btnDark.className = "color-mode-btn flex-1 bg-[#1E293B] border-2 border-[#2563EB] rounded-xl p-4 flex flex-col items-center justify-center space-y-2 text-[#3B82F6]";
                btnLight.className = "color-mode-btn flex-1 bg-[#F8FAFC] border-2 border-transparent rounded-xl p-4 flex flex-col items-center justify-center space-y-2 text-gray-400 hover:bg-gray-100 transition";
            } else {
                btnLight.className = "color-mode-btn flex-1 bg-white border-2 border-[#2563EB] rounded-xl p-4 flex flex-col items-center justify-center space-y-2 text-[#2563EB]";
                btnDark.className = "color-mode-btn flex-1 bg-[#E2E8F0] border-2 border-transparent rounded-xl p-4 flex flex-col items-center justify-center space-y-2 text-gray-500 hover:bg-gray-300 transition";
            }
        }
    }

    if (isDarkMode) document.body.classList.add('dark-mode');
    updateSettingsUI(isDarkMode);

    function setDarkModeState(state) {
        if (state) document.body.classList.add('dark-mode');
        else document.body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', state);
        updateSettingsUI(state);
    }

    if (darkModeToggles.length > 0) darkModeToggles.forEach(toggle => toggle.addEventListener('click', () => setDarkModeState(!document.body.classList.contains('dark-mode'))));

    const btnLight = document.getElementById('btnLightMode');
    const btnDark = document.getElementById('btnDarkMode');
    if (btnLight) btnLight.addEventListener('click', () => setDarkModeState(false));
    if (btnDark) btnDark.addEventListener('click', () => setDarkModeState(true));
});
