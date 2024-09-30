
# Pengecek Plagiasi

Pengecek Plagiasi adalah aplikasi desktop berbasis Python yang memungkinkan pengguna untuk membandingkan beberapa file kode sumber (atau dokumen lain) dan menghitung persentase kesamaan antara file-file tersebut. Aplikasi ini juga memberikan rekomendasi pengurangan nilai jika tingkat plagiarisme melebihi ambang batas yang telah ditentukan.

## Fitur Utama

- **Dukungan untuk berbagai format file:** Mendukung format `.txt`, `.pdf`, `.docx`, serta berbagai file kode pemrograman seperti `.py`, `.java`, `.cpp`, dan lainnya.
- **Perhitungan Persentase Kesamaan:** Aplikasi membandingkan teks dari dua atau lebih file dan menghitung persentase kesamaan.
- **Rekomendasi Pengurangan Nilai:** Jika kesamaan file melebihi ambang batas yang telah ditentukan, aplikasi akan memberikan rekomendasi pengurangan nilai.
- **Ekspor Hasil:** Hasil pengecekan dapat diekspor ke file Excel (`.xlsx`), menampilkan detail kesamaan antar file dan rekomendasi pengurangan nilai.
- **Antarmuka Pengguna Modern:** Menggunakan `CustomTkinter` untuk tampilan antarmuka yang modern dan intuitif.

## Screenshots


## Persyaratan Sistem

Sebelum menjalankan aplikasi ini, pastikan Anda memiliki:

- **Python 3.7+**
- Modul Python yang dibutuhkan (lihat bagian [Instalasi](#instalasi))

## Instalasi

1. Clone repositori ini ke komputer Anda:

   ```bash
   git clone https://github.com/alfikiafan/plagiarism-checker.git
   ```

2. Pindah ke direktori proyek:

   ```bash
   cd plagiarism-checker
   ```

3. Instal semua dependensi yang diperlukan:

   ```bash
   pip install -r requirements.txt
   ```

## Cara Menggunakan

1. Jalankan aplikasi dengan perintah berikut:

   ```bash
   python main.py
   ```

2. **Langkah-langkah dalam aplikasi:**
   - Pilih dua atau lebih file yang ingin Anda bandingkan menggunakan tombol `Browse`.
   - Masukkan ambang batas persentase kesamaan dan pengurangan nilai maksimal (default 80% dan 20%).
   - Tentukan lokasi file hasil ekspor dengan tombol `Browse` di bagian output.
   - Klik tombol `Mulai Pengecekan` untuk memproses file yang dipilih.
   - Aplikasi akan menampilkan hasil perbandingan dan memberikan rekomendasi pengurangan nilai, serta menyimpan hasil ke file Excel yang telah Anda tentukan.

## Struktur Proyek

Berikut adalah struktur folder dari proyek ini:

```
├── controller/
│   ├── plagiarism_controller.py
├── model/
│   ├── file_reader.py
│   ├── plagiarism_checker.py
├── view/
│   ├── comparison_display.py
|   ├── file_content_display.py
|   ├── file_selection.py
|   ├── main_window.py
|   ├── results_display.py
├── utils/
│   ├── __init__.py
│   ├── helpers.py
├── main.py
├── requirements.txt
└── README.md
```

- **`controller/`:** Berisi logika kontrol aplikasi, termasuk pemrosesan file dan koordinasi antara view dan model.
- **`model/`:** Menangani pembacaan file dan logika pengecekan plagiasi.
- **`view/`:** Menyediakan antarmuka pengguna berbasis `CustomTkinter`.
- **`utils/`:** Fungsi tambahan yang digunakan di seluruh aplikasi.
- **`main.py`:** Titik masuk aplikasi.

## Dependensi

Aplikasi ini bergantung pada beberapa pustaka Python. Berikut adalah daftar pustaka yang diperlukan (disimpan di `requirements.txt`):

- **customtkinter**: Antarmuka pengguna modern berbasis Tkinter.
- **python-docx**: Untuk membaca file `.docx`.
- **PyPDF2**: Untuk membaca file `.pdf`.
- **pandas**: Untuk manipulasi data dan ekspor hasil ke Excel.
- **openpyxl**: Untuk menulis file Excel.

## Contoh File Excel Output

Setelah proses pengecekan plagiasi selesai, file Excel yang dihasilkan akan memiliki dua sheet utama:

1. **Pengurangan Nilai:** Menampilkan persentase pengurangan nilai berdasarkan kesamaan file.
2. **Kesamaan:** Menampilkan persentase kesamaan antara dua file yang dibandingkan.

## Kontribusi

Kontribusi sangat disambut! Jika Anda ingin berkontribusi pada proyek ini:

1. Fork repositori ini.
2. Buat branch fitur baru (`git checkout -b fitur-baru`).
3. Commit perubahan Anda (`git commit -m 'Menambahkan fitur baru'`).
4. Push ke branch (`git push origin fitur-baru`).
5. Buat Pull Request.

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

## Kontak

Jika Anda memiliki pertanyaan atau saran, jangan ragu untuk menghubungi saya di [email@example.com](mailto:alfiki.diastama@gmail.com).
```