# Kompresaja

Kompresaja adalah aplikasi web intuitif yang dirancang untuk membantu pengguna mengecilkan ukuran dokumen dan berbagai jenis file secara cepat dan efisien, langsung dari browser.

## Fitur

- Mendukung berbagai format file (.txt, .docx, .pdf, .csv, gambar, dll)
- Drag & drop atau klik untuk memilih file
- Kompresi cepat dengan algoritma yang optimal
- Tampilan statistik kompresi (ukuran asli vs hasil)
- Unduh hasil kompresi dengan mudah
- Antarmuka responsif dan modern

## Teknologi

- Backend: Python (Flask)
- Frontend: HTML, CSS (Tailwind CSS), JavaScript
- Dependencies: Lihat `requirements.txt`

## Instalasi

1. Clone repositori ini
2. Buat virtual environment Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi:
   ```bash
   python app.py
   ```
5. Buka browser dan akses `http://localhost:5000`

## Penggunaan

1. Buka aplikasi di browser
2. Drag & drop file atau klik untuk memilih file
3. Tunggu proses kompresi selesai
4. Lihat statistik kompresi
5. Klik tombol unduh untuk mendapatkan file terkompresi

## Kontribusi

Silakan buat pull request untuk kontribusi. Untuk perubahan besar, harap buka issue terlebih dahulu untuk mendiskusikan perubahan yang diinginkan.

## Lisensi

[MIT](https://choosealicense.com/licenses/mit/) 