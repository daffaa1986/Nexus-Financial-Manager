const API_BASE = "http://127.0.0.1:8000";

document.addEventListener('DOMContentLoaded', function () {
    // 1. Temukan tombol "Upload Mutasi" di halaman ini secara dinamis
    const buttons = Array.from(document.querySelectorAll('button'));
    const uploadBtn = buttons.find(btn => 
        btn.textContent.includes('Upload Mutasi') || 
        btn.querySelector('span')?.textContent.includes('Upload Mutasi')
    );

    if (uploadBtn) {
        let fileInput = document.getElementById('fileUpload');
        if (!fileInput) {
            // Bungkus tombol dalam div relative untuk meletakkan input file transparan di atasnya
            const parent = uploadBtn.parentElement;
            const wrapper = document.createElement('div');
            wrapper.className = "relative inline-block";

            parent.replaceChild(wrapper, uploadBtn);
            wrapper.appendChild(uploadBtn);

            // Buat element input file
            fileInput = document.createElement('input');
            fileInput.type = "file";
            fileInput.id = "fileUpload";
            fileInput.title = "Upload Mutasi atau Struk";
            fileInput.setAttribute('aria-label', "Upload Mutasi atau Struk");
            fileInput.accept = ".pdf, .jpg, .jpeg, .png, .webp";
            fileInput.className = "absolute inset-0 w-full h-full opacity-0 cursor-pointer";
            wrapper.appendChild(fileInput);
        }

        bindUploadHandler(fileInput);
    }
});

function showToast(message, type = 'info', duration = 0) {
    let toast = document.getElementById('ai-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'ai-toast';
        toast.className = "fixed bottom-8 right-8 z-[9999] p-4 rounded-2xl shadow-2xl border backdrop-blur-md transition-all duration-300 transform translate-y-10 opacity-0 flex items-center space-x-3 text-xs md:text-sm font-semibold max-w-md";
        document.body.appendChild(toast);
    }

    const colors = {
        info: "bg-slate-900/90 text-white border-slate-700/50",
        success: "bg-emerald-950/95 text-emerald-200 border-emerald-500/30",
        error: "bg-red-950/95 text-red-200 border-red-500/30",
        warning: "bg-amber-950/95 text-amber-200 border-amber-500/30"
    };

    toast.className = `fixed bottom-8 right-8 z-[9999] p-4 rounded-2xl shadow-2xl border backdrop-blur-md transition-all duration-300 transform flex items-center space-x-3 text-xs md:text-sm font-semibold max-w-md ${colors[type] || colors.info}`;

    const icons = {
        info: '<i class="fas fa-spinner fa-spin text-blue-400 text-lg"></i>',
        success: '<i class="fas fa-check-circle text-emerald-400 text-lg"></i>',
        error: '<i class="fas fa-exclamation-circle text-red-400 text-lg"></i>',
        warning: '<i class="fas fa-exclamation-triangle text-amber-400 text-lg"></i>'
    };

    toast.innerHTML = `
        <div class="flex-shrink-0">${icons[type] || ''}</div>
        <div class="flex-1">${message}</div>
    `;

    setTimeout(() => {
        toast.classList.remove('translate-y-10', 'opacity-0');
        toast.classList.add('translate-y-0', 'opacity-100');
    }, 50);

    if (duration > 0) {
        setTimeout(() => {
            hideToast();
        }, duration);
    }
}

function hideToast() {
    const toast = document.getElementById('ai-toast');
    if (toast) {
        toast.classList.remove('translate-y-0', 'opacity-100');
        toast.classList.add('translate-y-10', 'opacity-0');
    }
}

function bindUploadHandler(fileInput) {
    fileInput.addEventListener('change', async function () {
        const file = this.files[0];
        if (!file) return;

        showToast(`Mempersiapkan unggahan file: ${file.name}...`, 'info');

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch(`${API_BASE}/api/upload`, {
                method: "POST",
                body: formData
            });
            const result = await response.json();

            // 1. Cek jika file duplikat (terdeteksi via hash di backend)
            if (result.status === 'duplicate') {
                showToast(`❌ Duplikat: ${result.message}`, 'error', 5000);
                this.value = '';
                return;
            }

            // 2. Hubungkan ke WebSocket untuk mendengarkan proses background secara real-time
            connectWebSocket(file.name);

        } catch (error) {
            showToast("Gagal terhubung ke API server. Pastikan server Python menyala!", "error", 4000);
            this.value = '';
        }
    });
}

function connectWebSocket(filename) {
    const socket = new WebSocket(`ws://${API_BASE.replace('http://', '')}/ws/updates`);

    socket.onmessage = function (event) {
        const response = JSON.parse(event.data);

        if (response.status === "loading") {
            showToast(response.message, 'info');
        } else if (response.status === "success") {
            showToast(response.data?.message || "File berhasil diproses!", 'success', 3000);
            
            // Tunggu 2 detik kemudian reload halaman untuk memuat data terbaru
            setTimeout(() => {
                location.reload();
            }, 2000);
            
            socket.close();
        } else if (response.status === "error") {
            showToast(response.data?.message || "Terjadi kesalahan saat memproses file.", 'error', 5000);
            socket.close();
        }
    };

    socket.onopen = function () {
        console.log("WebSocket terhubung untuk file:", filename);
    };

    socket.onerror = function (err) {
        console.error("WebSocket error:", err);
    };
}
