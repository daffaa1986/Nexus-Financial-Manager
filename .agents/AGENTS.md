# Aturan Perilaku & Pedoman Proyek: Nexus Finance AI

File ini mendefinisikan aturan perilaku, alur kerja AI/ML, panduan pengembangan, dan konfigurasi teknis untuk asisten AI (Antigravity) dalam mengelola dan mengembangkan proyek **Nexus Finance AI**.

---

## 🚀 1. Panduan Menjalankan API Server (FastAPI)

Asisten AI harus selalu mengarahkan pengguna atau mengingat cara menjalankan server API sebagai berikut:
1. **Pindah ke Direktori Backend:**
   ```bash
   cd backend
   ```
2. **Instalasi Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Konfigurasi Environment (.env):**
   * Pastikan file `.env` diisi berdasarkan template `.env.example`.
   * Variabel utama: `GEMINI_API_KEY` (harus berisi API Key Google AI Studio yang valid).
4. **Jalankan Aplikasi:**
   ```bash
   python main.py
   ```
   *Alternatif:* `uvicorn main:app --reload --port 8000`
5. **Dokumentasi API:** Tersedia secara interaktif di `http://127.0.0.1:8000/docs`.

---

## 🧠 2. Alur Kerja (Pipeline) AI/ML

Sistem ini memproses dua jenis input finansial:
1. **Mutasi Rekening (PDF):**
   * Pembersihan teks menggunakan fungsi `nlp_bersihkan_teks()` untuk menyaring kode transfer perbankan yang tidak relevan.
   * Kategorisasi menggunakan pendekatan hibrida: pencocokan kata kunci cepat (`KATEGORI_KEYWORDS`) → jika gagal, gunakan fallback LLM `gemini-1.5-flash`.
2. **Struk Belanjaan (Gambar/OCR):**
   * Upload gambar (`.jpg`, `.png`, `.webp`) otomatis dialihkan ke endpoint OCR.
   * Model `gemini-1.5-flash` (Gemini Vision) memproses gambar struk dan mengekstrak objek JSON terstruktur (item, harga, kuantitas, pajak, total).
3. **Analisis Finansial (Spending Analyzer):**
   * Membaca transaksi dari database SQLite (`nexus_finance.db`).
   * Menghitung indikator **Bocor** (pengeluaran kecil tapi sering) dan **Boros** (pengeluaran kategori dominan >40% atau transaksi tunggal besar).

---

## 🛠️ 3. Pedoman Coding & Keamanan (Coding Standards)

Setiap modifikasi kode di masa mendatang harus mematuhi aturan berikut:
* **Tidak Ada Hardcoded Secrets:** Jangan pernah menuliskan API Key langsung di dalam file `.py` atau `.js`. Selalu gunakan `os.environ.get()` dan pastikan dimuat melalui `load_dotenv()` di awal program.
* **Penamaan Variabel & Penghindaran Keyword Bentrokan:** Hindari penamaan variabel lokal yang menimpa fungsi built-in Python (misal: gunakan `tipe` sebagai pengganti `type`).
* **Autentikasi & Keamanan:** Seluruh rute API di `main.py` harus dikembangkan menuju sistem multi-user dengan autentikasi JWT di fase berikutnya.
* **Penanganan Error:** Terapkan try-catch yang kuat pada parser regex dan pemrosesan PDF agar server tidak crash jika berkas mutasi memiliki format yang berbeda.

---

## 🎨 4. Desain & Antarmuka (Aesthetics & Responsiveness)

* **Mobile-First Responsive Web:** Saat memodifikasi CSS/HTML di frontend, pastikan menu navigasi samping (sidebar) bersifat collapsible (dapat disembunyikan dengan hamburger menu) di layar berukuran mobile (<980px).
* **Mata Uang Konsisten:** Gunakan format mata uang Rupiah (`Rp 12.345`) secara konsisten di seluruh halaman, hindari pencampuran dengan simbol dollar (`$`) di area visual dashboard utama.
