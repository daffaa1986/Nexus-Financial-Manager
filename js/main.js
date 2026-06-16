document.addEventListener('DOMContentLoaded', function () {
    // ==========================================
    // 1. INISIALISASI GRAFIK KOSONG (Menunggu Data)
    // ==========================================
    let expenseRadarChart;

    const radarElement = document.getElementById('radarChart');
    if (radarElement) {
        const radarCtx = radarElement.getContext('2d');
        expenseRadarChart = new Chart(radarCtx, {
            type: 'radar',
            data: {
                labels: ['Menunggu Data...'], // Akan diganti oleh AI
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

    // 2. MIXED CHART - Balance Momentum
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
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        display: false,
                        beginAtZero: true
                    },
                    x: {
                        grid: { display: false },
                        border: { display: false },
                        ticks: {
                            color: '#94A3B8',
                            font: { size: 9, weight: 'bold' }
                        }
                    }
                }
            }
        });
    }

    // js untuk time-analysis
    const timeElement = document.getElementById('timeBarChart');
    if (timeElement) {
        const ctx = timeElement.getContext('2d');

        // Meniru gaya bar chart di desain SVG (Rounded & Light Blue)
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'],
                datasets: [{
                    label: 'Process Time (ms)',
                    data: [120, 190, 150, 250, 180, 210, 320, 240, 170, 200],
                    backgroundColor: '#DAE2FD', // Warna biru muda sesuai SVG
                    hoverBackgroundColor: '#497CFF',
                    borderRadius: 10,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { display: true, color: 'rgba(200, 200, 200, 0.1)' },
                        border: { display: false }
                    },
                    x: {
                        grid: { display: false },
                        border: { display: false }
                    }
                }
            }
        });
    }

    // js untuk category manager
    const cards = document.querySelectorAll('.category-card');
    const inputName = document.getElementById('input-name');
    const inputBudget = document.getElementById('input-budget');
    const previewTitle = document.getElementById('preview-title');
    const colorOptions = document.querySelectorAll('.color-option');
    const iconOptions = document.querySelectorAll('.icon-option');

    function updateSelectionColors(color) {
        const previewIcon = document.querySelector('.preview-icon');
        if (!previewIcon) return;
        const colorMap = {
            blue: '#EFF6FF',
            red: '#FEF2F2',
            green: '#ECFDF5',
            purple: '#FAF5FF',
            orange: '#FFF7ED'
        };
        const textMap = {
            blue: '#2563EB',
            red: '#B91C1C',
            green: '#047857',
            purple: '#7C3AED',
            orange: '#EA580C'
        };
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
        cards.forEach(card => {
            card.addEventListener('click', () => setActiveCard(card));
        });

        const activeCard = document.querySelector('.category-card.active');
        if (activeCard) setActiveCard(activeCard);
    }

    if (inputName) {
        inputName.addEventListener('input', (e) => {
            if(previewTitle) previewTitle.innerText = e.target.value;
            const activeCardTitle = document.querySelector('.category-card.active h4');
            if (activeCardTitle) activeCardTitle.innerText = e.target.value;
        });
    }

    if (inputBudget) {
        inputBudget.addEventListener('blur', (e) => {
            const value = e.target.value.replace(/[^0-9.]/g, '');
            if (!value) return;
            e.target.value = parseFloat(value).toLocaleString('en-US', { minimumFractionDigits: 2 });
        });
    }

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

    // js untuk settings
    // Add smooth scrolling for sub-nav links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Sub-nav active state toggling
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    const sections = document.querySelectorAll('main section');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            // Adjusted margin logic for when you scroll
            if (scrollY >= (sectionTop - sectionHeight / 3)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            // Reset all classes
            link.classList.remove('bg-[#EEF2FF]', 'text-[#2563EB]', 'font-bold', 'bg-red-50');
            if (link.getAttribute('href') !== '#critical') {
                link.classList.add('text-gray-500');
            } else {
                link.classList.add('text-[#BA1A1A]');
            }
            
            // Add active class if matched
            if (link.getAttribute('href') === `#${current}`) {
                if (current === 'critical') {
                    link.classList.add('bg-red-50', 'font-bold');
                } else {
                    link.classList.remove('text-gray-500');
                    link.classList.add('bg-[#EEF2FF]', 'text-[#2563EB]', 'font-bold');
                }
            }
        });
    }, { passive: true });

    // ==========================================
    // 2. MENGAMBIL DATA & MENGGERAKKAN DASHBOARD
    // ==========================================
    async function muatDataDariDatabase() {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/transactions");
            const result = await response.json();

            if (result.status === "success" && result.data.length > 0) {
                // Variabel untuk menghitung uang
                let totalIncome = 0;
                let totalExpense = 0;
                let categorySums = {}; // Untuk menyimpan total per kategori (Radar Chart)

                const tableBody = document.querySelector('table tbody');
                if (tableBody) tableBody.innerHTML = ''; 

                result.data.forEach(trx => {
                    // MENGHITUNG TOTAL UANG
                    let type = trx.type;
                    if (!type) {
                        type = trx.category === 'Income' ? 'CR' : 'DB';
                    }

                    if (type === 'CR') {
                        totalIncome += trx.amount;
                    } else if (type === 'DB') {
                        totalExpense += trx.amount;
                        // Menjumlahkan pengeluaran berdasarkan Kategori dari AI Gemini
                        let cat = trx.category || "Lainnya";
                        // Jangan tambahkan Income ke pengeluaran
                        if(cat !== 'Income') {
                            categorySums[cat] = (categorySums[cat] || 0) + trx.amount;
                        }
                    }

                    // MENGISI TABEL (Sama seperti sebelumnya)
                    if (tableBody) {
                        const newRow = document.createElement('tr');
                        newRow.className = "border-b border-gray-50 group hover:bg-slate-50 transition";
                        const formattedAmount = "Rp " + parseFloat(trx.amount).toLocaleString('id-ID');
                        const isExpense = type === 'DB';
                        const colorClass = isExpense ? 'text-red-500' : 'text-green-500';
                        const sign = isExpense ? '-' : '+';

                        newRow.innerHTML = `
                            <td class="py-4 px-2 font-bold">${trx.date}</td>
                            <td class="py-4 px-2 text-gray-800 font-bold">${trx.label}</td>
                            <td class="py-4 px-2 text-gray-500">${trx.category}</td>
                            <td class="py-4 px-2 font-bold text-right ${colorClass}">${sign}${formattedAmount}</td>
                            <td class="py-4 px-2 text-right"><span class="bg-blue-50 text-blue-600 text-[9px] px-2 py-1 rounded-md uppercase font-black shadow-sm">AI Scanned</span></td>
                        `;
                        tableBody.appendChild(newRow);
                    }
                });

                // ==========================================
                // 3. MENYUNTIKKAN HASIL HITUNGAN KE HTML & GRAFIK
                // ==========================================
                
                // Update Kotak Angka (Cari elemen berdasarkan teks HTML-nya)
                const incomeBox = document.querySelector('.bg-green-50')?.parentElement?.querySelector('h4');
                const expenseBox = document.querySelector('.bg-red-50')?.parentElement?.querySelector('h4');
                const mainBalanceBox = document.querySelector('h3.text-5xl.font-black');

                // Jika elemen tidak ditemukan (misal di hal lain), lewati
                if (incomeBox) incomeBox.innerHTML = `Rp ${totalIncome.toLocaleString('id-ID')}`;
                if (expenseBox) expenseBox.innerHTML = `Rp ${totalExpense.toLocaleString('id-ID')}`;
                
                let sisaSaldo = totalIncome - totalExpense;
                if (mainBalanceBox) {
                    mainBalanceBox.innerHTML = `Rp ${sisaSaldo.toLocaleString('id-ID')} <span class="text-2xl text-gray-400 font-medium">.00</span>`;
                }

                // Update Radar Chart Expense Architecture
                if (expenseRadarChart && Object.keys(categorySums).length > 0) {
                    expenseRadarChart.data.labels = Object.keys(categorySums); // Label Kategori dari Gemini
                    expenseRadarChart.data.datasets[0].data = Object.values(categorySums); // Nominal Uangnya
                    expenseRadarChart.update(); // Perintahkan Chart.js untuk menggambar ulang!
                }
            }
        } catch (error) {
            console.error("Belum bisa mengambil data:", error);
        }
    }

    muatDataDariDatabase();

    // ==========================================
    // 4. KONEKSI WEBSOCKET (UPLOAD FILE)
    // ==========================================
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/updates");
    
    socket.onmessage = function(event) {
        const response = JSON.parse(event.data);
        const uploadBtn = document.getElementById('fileUpload') ? document.getElementById('fileUpload').previousElementSibling : null;

        if (response.status === "loading") {
            if (uploadBtn) {
                uploadBtn.innerHTML = `<i class="fas fa-spinner fa-spin text-sm"></i><span>${response.message}</span>`;
                uploadBtn.classList.add('opacity-80', 'cursor-not-allowed');
            }
        } else if (response.status === "success") {
            if (uploadBtn) {
                uploadBtn.innerHTML = `<i class="fas fa-plus-circle text-sm"></i><span>Upload Mutasi</span>`;
                uploadBtn.classList.remove('opacity-80', 'cursor-not-allowed');
            }
            // Jika berhasil upload, muat ulang data dari database agar grafik & angka update otomatis!
            muatDataDariDatabase(); 
        }
    };

    const fileInput = document.getElementById('fileUpload');
    if (fileInput) {
        fileInput.addEventListener('change', async function() {
            const file = this.files[0];
            if (!file) return;
            const formData = new FormData();
            formData.append("file", file);
            try {
                await fetch("http://127.0.0.1:8000/api/upload", { method: "POST", body: formData });
                this.value = ''; 
            } catch (error) {
                alert("Server Python terputus!");
            }
        });
    }

    // ==========================================
    // 5. EDIT PROFILE BUTTON LOGIC
    // ==========================================
    const editProfileBtn = document.getElementById('editProfileBtn');
    if (editProfileBtn) {
        const profileInputs = document.querySelectorAll('#fullName, #emailAddress, #phoneNumber, #architectBio');
        const profileSelects = document.querySelectorAll('#timezone');
        
        // Initial state: readonly/disabled + visual cue
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
                
                profileInputs.forEach(input => {
                    input.removeAttribute('readonly');
                    input.classList.remove('bg-slate-50', 'text-slate-500', 'cursor-not-allowed');
                    input.classList.add('bg-white', 'ring-2', 'ring-blue-100');
                });
                profileSelects.forEach(select => {
                    select.removeAttribute('disabled');
                    select.classList.remove('bg-slate-50', 'text-slate-500', 'cursor-not-allowed');
                    select.classList.add('bg-white', 'ring-2', 'ring-blue-100');
                });
            } else {
                editProfileBtn.innerHTML = 'Edit Profile';
                editProfileBtn.classList.replace('bg-[#2563EB]', 'bg-[#EEF2FF]');
                editProfileBtn.classList.replace('text-white', 'text-[#2563EB]');
                
                profileInputs.forEach(input => {
                    input.setAttribute('readonly', 'true');
                    input.classList.add('bg-slate-50', 'text-slate-500', 'cursor-not-allowed');
                    input.classList.remove('bg-white', 'ring-2', 'ring-blue-100');
                });
                profileSelects.forEach(select => {
                    select.setAttribute('disabled', 'true');
                    select.classList.add('bg-slate-50', 'text-slate-500', 'cursor-not-allowed');
                    select.classList.remove('bg-white', 'ring-2', 'ring-blue-100');
                });
            }
        });
    }

    // ==========================================
    // 6. DARK MODE LOGIC
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

    if (isDarkMode) {
        document.body.classList.add('dark-mode');
    }
    updateSettingsUI(isDarkMode);

    function setDarkModeState(state) {
        if (state) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
        localStorage.setItem('darkMode', state);
        updateSettingsUI(state);
    }

    if (darkModeToggles.length > 0) {
        darkModeToggles.forEach(toggle => {
            toggle.addEventListener('click', () => {
                const newState = !document.body.classList.contains('dark-mode');
                setDarkModeState(newState);
            });
        });
    }

    const btnLight = document.getElementById('btnLightMode');
    const btnDark = document.getElementById('btnDarkMode');
    if (btnLight) btnLight.addEventListener('click', () => setDarkModeState(false));
    if (btnDark) btnDark.addEventListener('click', () => setDarkModeState(true));

});