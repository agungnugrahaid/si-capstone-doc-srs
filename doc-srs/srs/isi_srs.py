"""Isi dokumen SRS SAPA v1.1 (Bab I-VI, Daftar Pustaka, Lampiran).

Ditulis mengikuti profil gaya tulis Agung (Cekula/_writing-profile/writing-style.md):
bahasa Indonesia baku, kalimat lugas, daftar diawali kalimat pengantar, istilah teknis dalam bahasa Inggris,
sitasi APA 7. Identitas anggota dan dosen tidak disimpan di sini (repo publik); lihat srs-identitas.json di Drive.

Blok yang dipakai build_srs.py:
  ("h1", "BAB I", "PENDAHULUAN", "1")      bab baru; argumen ke-4 = kunci penomoran tabel/gambar
  ("h2", teks) / ("h3", teks)
  ("p", teks)                               paragraf rata kiri-kanan, indentasi baris pertama
  ("ol", [butir]) / ("ul", [butir])         daftar bernomor / berbutir; "**Label.** isi" ditebalkan
  ("table", kunci, judul, header, baris, lebar_cm)
  ("kv", kunci, judul, baris)               tabel dua kolom Elemen | Keterangan
  ("fig", kunci, judul, berkas_png, penjelasan)
Rujukan silang ditulis {tab:kunci} atau {fig:kunci} dan diganti nomor saat build.
Teks [ISI: ...] diberi stabilo kuning sebagai placeholder yang harus diisi.
"""

PNG = "diagram/png/"
MOCK = "final/mockup/"

UC = [  # (nomor, nama, aktor, kode F)
    ("UC-01", "Login", "Agen/CS, Supervisor, Administrator", "F01"),
    ("UC-02", "Mengirim Pesan WhatsApp", "Pelanggan, WhatsApp Web", "F02, F03"),
    ("UC-03", "Menjawab Pesan Otomatis dengan AI", "Penyedia AI, WhatsApp Web", "F04, F05, F06"),
    ("UC-04", "Mengelola Percakapan", "Agen/CS", "F07"),
    ("UC-05", "Mengelola Prospek", "Agen/CS", "F08"),
    ("UC-06", "Mengelola Kontak Pelanggan", "Agen/CS", "F09"),
    ("UC-07", "Melihat Dashboard Pemantauan", "Supervisor, Administrator", "F10"),
    ("UC-08", "Mengelola Nomor WhatsApp", "Administrator", "F11"),
    ("UC-09", "Mengelola Basis Pengetahuan", "Supervisor, Administrator", "F12"),
    ("UC-10", "Mengatur AI dan Anti-ban", "Administrator", "F13"),
    ("UC-11", "Mengelola Tim dan Hak Akses", "Administrator", "F14"),
    ("UC-12", "Melihat Log Audit", "Supervisor, Administrator", "F15"),
]

B = []


def add(*blk):
    B.append(blk)


# ====================================================================== BAB I
add("h1", "BAB I", "PENDAHULUAN", "1")
add("h2", "1.1 Latar Belakang")
add("p", "Bimbingan Belajar Asentra merupakan penyedia jasa pendidikan nonformal di Kecamatan Gondang, Kabupaten "
         "Sragen, yang berdiri pada tahun 2024. Asentra melayani 128 siswa aktif dari jenjang pra-sekolah sampai SMA "
         "dengan 24 pengajar, satu admin, dan dua sales. Layanan yang ditawarkan terdiri atas kelas eksklusif, program "
         "reguler, dan kelas persiapan tes kemampuan akademik.")
add("p", "Calon siswa dan orang tua menghubungi Asentra melalui WhatsApp. Pertanyaan masuk ke lebih dari satu nomor, "
         "yaitu nomor admin dan nomor sales, dan setiap nomor dipegang pada ponsel yang berbeda. Pengumpulan kebutuhan "
         "(requirement gathering) bersama pemilik Asentra menemukan permasalahan sebagai berikut.")
add("ol", [
    "**Percakapan tidak terpantau.** Tidak diketahui berapa percakapan masuk pada tiap nomor, siapa yang menangani, "
    "dan percakapan mana yang belum dibalas, sehingga calon siswa dapat menunggu tanpa kepastian.",
    "**Pertanyaan berulang dijawab manual.** Pertanyaan tentang jadwal, biaya, fasilitas, dan cara pendaftaran dijawab "
    "satu per satu dari ponsel, sehingga kecepatan balasan bergantung pada siapa yang sedang memegang nomor.",
    "**Informasi program tidak terstruktur.** Informasi program hanya beredar sebagai kartu gambar di percakapan, "
    "sehingga admin mengirim ulang informasi yang sama berkali-kali.",
    "**Riwayat percakapan tersebar.** Percakapan tersimpan di beberapa perangkat tanpa riwayat terpusat dan tanpa "
    "pembagian hak akses per nomor, sehingga serah terima pekerjaan antarstaf sulit dilakukan.",
    "**Data calon siswa tidak tercatat.** Tindak lanjut bergantung pada ingatan staf, sehingga peluang pendaftaran "
    "dapat hilang tanpa terdeteksi.",
])
add("p", "WhatsApp tetap dipertahankan sebagai kanal utama. Pelanggan memilih kanal berdasarkan kemudahan dan kecepatan, "
         "sehingga memperbaiki mutu kanal yang sudah dipakai lebih tepat daripada menambah kanal baru (Wolf & "
         "Steul-Fischer, 2023). Teknik retrieval-augmented generation (RAG) memungkinkan chatbot menjawab berdasarkan "
         "dokumen resmi organisasi sehingga sumber jawaban dapat ditelusuri (Fan dkk., 2024). Chatbot WhatsApp "
         "berbasis RAG juga telah diterapkan untuk menjawab pertanyaan dari dokumen aturan organisasi di Indonesia "
         "(Imaduddin dkk., 2026).")
add("p", "Berdasarkan permasalahan tersebut, Kelompok 1 merancang SAPA (Sistem Asisten Pelanggan dan Akuisisi). SAPA "
         "adalah aplikasi web berbasis Laravel yang menautkan beberapa nomor WhatsApp Asentra melalui pemindaian kode "
         "QR dan menyatukan seluruh percakapan dalam satu kotak masuk. SAPA menjawab pertanyaan berulang dari basis "
         "pengetahuan resmi mitra beserta sumbernya, mencatat data calon siswa dari isi percakapan, dan menampilkan "
         "dashboard pemantauan per nomor.")

add("h2", "1.2 Rumusan Masalah")
add("p", "Rumusan masalah yang dijawab oleh sistem adalah sebagai berikut.")
add("ol", [
    "Bagaimana menyatukan beberapa nomor WhatsApp milik Bimbingan Belajar Asentra ke dalam satu kotak masuk sehingga "
    "seluruh percakapan dan data calon siswa tersimpan terpusat?",
    "Bagaimana menyediakan pemantauan per nomor WhatsApp yang menampilkan volume percakapan, waktu balas pertama, "
    "percakapan belum dibalas, dan konversi menjadi pendaftaran?",
    "Bagaimana menerapkan kecerdasan artifisial yang menjawab pertanyaan dari basis pengetahuan resmi, mengenali maksud "
    "pesan, mengisi data calon siswa, dan menentukan prioritas tindak lanjut dengan alasan yang dapat diperiksa?",
    "Bagaimana menerapkan kontrol akses berbasis role per nomor WhatsApp serta menjaga pengiriman pesan tetap aman dari "
    "pembatasan nomor dan sesuai aturan pelindungan data pribadi?",
])

add("h2", "1.3 Tujuan Dokumen")
add("p", "Dokumen Software Requirements Specification (SRS) ini bertujuan untuk merinci kebutuhan sistem SAPA, yaitu "
         "fungsi, batasan, antarmuka, dan data yang harus dipenuhi. Dokumen menjadi acuan bersama bagi tim pengembang, "
         "dosen pengampu, dan mitra pada tahap perancangan, pengembangan, dan pengujian. Susunan kebutuhan mengikuti "
         "IEEE Std 830-1998 (IEEE, 1998) dan ISO/IEC/IEEE 29148:2018 (ISO/IEC/IEEE, 2018) yang disesuaikan dengan "
         "template SRS Program Studi Sistem Informasi UMBY.")

add("h2", "1.4 Sasaran Pembaca")
add("p", "Dokumen ini ditujukan untuk pihak-pihak sebagai berikut.")
add("ul", [
    "**Tim pengembang**, sebagai acuan saat merancang, membangun, dan meninjau kode.",
    "**Dosen pengampu**, untuk menilai kelengkapan dan kelayakan kebutuhan sistem.",
    "**Mitra**, untuk memastikan kebutuhan Asentra sudah tertangkap dengan benar sebelum Sprint Review.",
    "**Penguji (tester)**, sebagai dasar penyusunan skenario uji pada Lampiran A.",
])

add("h2", "1.5 Ruang Lingkup Sistem")
add("p", "Ruang lingkup SAPA, termasuk hal yang tidak dikerjakan pada rilis ini, dirangkum pada {tab:lingkup}.")
add("table", "lingkup", "Ruang Lingkup Sistem", ["Aspek", "Keterangan"], [
    ["Nama sistem", "SAPA (Sistem Asisten Pelanggan dan Akuisisi)"],
    ["Deskripsi singkat", "Aplikasi web untuk Bimbingan Belajar Asentra yang menautkan beberapa nomor WhatsApp melalui "
     "kode QR ke dalam satu kotak masuk, dilengkapi jawaban otomatis berbasis AI, CRM calon siswa, dan dashboard "
     "pemantauan layanan."],
    ["Pengguna", "Admin dan sales (Agen/CS), supervisor, dan administrator sistem. Pelanggan (calon siswa atau orang tua) "
     "tidak memakai aplikasi web dan berinteraksi melalui WhatsApp."],
    ["Fungsi utama", "Login dan kontrol akses per nomor; penautan nomor WhatsApp; kotak masuk dan balasan; jawaban "
     "otomatis dari basis pengetahuan beserta sumber; eskalasi ke agen; pengelolaan prospek dan kontak; mesin anti-ban; "
     "dashboard per nomor; pengelolaan tim dan akses; log audit."],
    ["Di luar cakupan", "Pesan promosi massal (broadcast); kanal selain WhatsApp; WhatsApp Business API resmi; aplikasi "
     "mobile native; pembayaran dan data akademik siswa; two-factor authentication (2FA)."],
    ["Stakeholder", "Pemilik Asentra (Greta); admin dan sales Asentra; Product Owner dan tim pengembang Kelompok 1; "
     "dosen pengampu."],
], [3.5, 11.5])
add("p", "Bagian di luar cakupan dicatat agar mitra tidak mengharapkan fitur yang belum disepakati. Butir tersebut juga "
         "dicatat sebagai kebutuhan berprioritas Won't have pada {tab:fr}.")

add("h2", "1.6 Definisi, Akronim, dan Singkatan")
add("p", "Istilah yang dipakai dalam dokumen ini dijelaskan pada {tab:istilah}.")
add("table", "istilah", "Definisi, Akronim, dan Singkatan", ["Istilah", "Penjelasan"], [
    ["SRS", "Software Requirements Specification, dokumen spesifikasi kebutuhan perangkat lunak."],
    ["SAPA", "Sistem Asisten Pelanggan dan Akuisisi, nama sistem yang dikembangkan."],
    ["Laravel", "Framework PHP berpola Model-View-Controller (MVC) yang dipakai untuk aplikasi web SAPA."],
    ["MVC", "Model-View-Controller, pola yang memisahkan data (Model), tampilan (View), dan logika proses (Controller)."],
    ["Blade", "Template engine bawaan Laravel untuk menyusun halaman antarmuka."],
    ["WA Gateway", "Layanan Node.js terpisah yang menjalankan pustaka Baileys untuk menghubungkan SAPA ke WhatsApp Web."],
    ["Baileys", "Pustaka open source yang menghubungkan aplikasi ke WhatsApp Web sehingga nomor dapat ditautkan lewat QR."],
    ["QR", "Quick Response code, kode yang dipindai dari ponsel untuk menautkan nomor WhatsApp ke SAPA."],
    ["RAG", "Retrieval-Augmented Generation, teknik menyusun jawaban dengan mengambil dokumen sumber terlebih dahulu."],
    ["FTS5 / bm25", "Fitur pencarian teks penuh SQLite dan rumus peringkat yang dipakai untuk menemukan artikel basis "
     "pengetahuan."],
    ["Basis pengetahuan", "Kumpulan artikel resmi mitra (program, jadwal, biaya, fasilitas, pendaftaran) yang menjadi "
     "sumber jawaban AI."],
    ["Ambang keyakinan", "Batas nilai keyakinan AI. Di bawah batas ini AI tidak membalas dan percakapan dialihkan ke agen."],
    ["Eskalasi", "Pengalihan percakapan dari AI ke agen manusia."],
    ["CRM", "Customer Relationship Management, pengelolaan data dan tindak lanjut calon siswa."],
    ["Prospek", "Calon siswa yang sedang ditindaklanjuti, dengan tahap baru, dihubungi, tertarik, penawaran, daftar, "
     "dan batal."],
    ["Skor prioritas", "Nilai dari lima komponen berbobot yang menentukan prospek mana yang didahulukan."],
    ["RBAC", "Role-Based Access Control, kontrol akses berdasarkan role (peran); pada SAPA juga per nomor WhatsApp."],
    ["Anti-ban", "Mekanisme pembatas laju dan jeda pengiriman agar nomor WhatsApp mitra tidak diblokir."],
    ["OLTP / OLAP", "Online Transaction Processing (pencatatan transaksi harian seperti pesan dan prospek) dan Online "
     "Analytical Processing (ringkasan untuk analisis seperti metrik harian)."],
    ["2FA", "Two-factor authentication, verifikasi login dengan faktor kedua seperti kode OTP."],
    ["ERD", "Entity Relationship Diagram, diagram struktur tabel dan relasi basis data."],
    ["VPS", "Virtual Private Server, server virtual tempat aplikasi dijalankan."],
    ["MoSCoW", "Metode prioritas: Must have, Should have, Could have, Won't have."],
    ["PBI / SP", "Product Backlog Item dan Story Point, butir pekerjaan pada backlog dan ukuran relatif besarnya."],
    ["UAT", "User Acceptance Testing, pengujian penerimaan oleh pengguna mitra."],
    ["UC / US / F / NF", "Kode use case, user story, kebutuhan fungsional, dan kebutuhan non-fungsional."],
], [3.5, 11.5])

add("h2", "1.7 Referensi")
add("p", "Dokumen dan sumber yang dipakai dalam penyusunan SRS ini adalah sebagai berikut.")
add("ul", [
    "Form Usulan Judul Capstone Project Kelompok 1, 24 September 2026.",
    "Laporan Capstone Project Kelompok 1 (ASN1), 9 Oktober 2026, beserta catatan revisi dosen tanggal 7 Oktober 2026.",
    "Perencanaan Sprint Scrum SAPA (Product Backlog, Sprint Backlog, Sprint Planning, serta Tim dan Peran), 26 Oktober "
    "2026.",
    "SRS SAPA versi 1.0, 16 November 2026.",
    "Hasil wawancara dengan pemilik Bimbingan Belajar Asentra (Greta), 26 September 2026 (Lampiran B).",
    "IEEE Std 830-1998 (IEEE, 1998) dan ISO/IEC/IEEE 29148:2018 (ISO/IEC/IEEE, 2018).",
    "The Scrum Guide (Schwaber & Sutherland, 2020).",
    "Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (Republik Indonesia, 2022).",
])
add("p", "Sumber pustaka ditulis dengan format APA edisi ketujuh dan dicantumkan lengkap pada Daftar Pustaka.")

add("h2", "1.8 Sistematika Dokumen")
add("p", "Dokumen ini terdiri atas enam bab dan tiga lampiran. Bab I berisi pendahuluan. Bab II memberikan gambaran "
         "umum sistem. Bab III merinci kebutuhan fungsional, kebutuhan non-fungsional, antarmuka eksternal, dan "
         "kebutuhan data. Bab IV menyajikan model analisis berupa arsitektur, diagram UML untuk kedua belas use case, "
         "dan ERD. Bab V berisi rancangan antarmuka, dan Bab VI menjelaskan metode pengembangan Scrum. Lampiran A "
         "memuat matriks keterlacakan, Lampiran B hasil requirement gathering dalam format notulen rapat, dan Lampiran C "
         "daftar hal yang belum ditentukan.")

# ====================================================================== BAB II
add("h1", "BAB II", "DESKRIPSI UMUM SISTEM", "2")
add("h2", "2.1 Perspektif Produk")
add("p", "SAPA merupakan aplikasi web yang berdiri sendiri dan dikembangkan khusus untuk Bimbingan Belajar Asentra. "
         "SAPA tidak mengganti nomor WhatsApp yang sudah dipakai mitra. Nomor tersebut ditautkan ke SAPA melalui "
         "pemindaian kode QR, sehingga pelanggan tetap menghubungi nomor yang sama.")
add("p", "Aplikasi utama dibangun dengan Laravel 12 (PHP 8.2) dan basis data SQLite yang dilengkapi pencarian teks "
         "penuh FTS5. Hubungan ke WhatsApp ditangani oleh WA Gateway, yaitu layanan Node.js terpisah yang menjalankan "
         "pustaka Baileys, karena Baileys hanya tersedia untuk Node.js. Laravel dan WA Gateway saling berkirim data "
         "melalui HTTP lokal dalam format JSON. Penyedia AI (OpenAI, layanan yang kompatibel dengan OpenAI, atau "
         "Gemini) bersifat opsional; tanpa penyedia AI, sistem memakai mode aturan bawaan. Hubungan antarkomponen "
         "ditunjukkan pada {fig:arsitektur}.")
add("p", "Perubahan proses sebelum dan sesudah SAPA diterapkan dirangkum pada {tab:banding}.")
add("table", "banding", "Perbandingan Proses Sebelum dan Sesudah SAPA", ["Aspek", "Sebelum SAPA", "Sesudah SAPA"], [
    ["Kanal", "Beberapa nomor WhatsApp di ponsel berbeda", "Semua nomor tertaut dan tampil dalam satu kotak masuk"],
    ["Pertanyaan berulang", "Dijawab manual oleh admin atau sales", "Dijawab AI dari basis pengetahuan beserta sumber; "
     "pertanyaan sulit dialihkan ke agen"],
    ["Data calon siswa", "Tidak tercatat", "Kontak dan prospek dibuat otomatis dari percakapan"],
    ["Tindak lanjut", "Bergantung pada ingatan staf", "Papan prospek per tahap dengan skor prioritas"],
    ["Pemantauan", "Tidak ada", "Dashboard per nomor: volume, waktu balas pertama, belum dibalas, konversi"],
    ["Hak akses", "Siapa pun yang memegang ponsel", "Role dan akses per nomor ditegakkan di server, tercatat di log audit"],
], [3.2, 5.6, 6.2])

add("h2", "2.2 Fungsi Produk")
add("p", "Secara garis besar, SAPA menyediakan fitur sebagai berikut.")
add("ul", [
    "Autentikasi dan kontrol akses berlapis, yaitu berdasarkan role dan berdasarkan nomor WhatsApp.",
    "Penautan dan pemantauan nomor WhatsApp melalui kode QR.",
    "Kotak masuk untuk membaca, membalas, mengambil alih, dan menyelesaikan percakapan.",
    "Jawaban otomatis dari basis pengetahuan resmi beserta sumber, klasifikasi maksud pesan, dan eskalasi ke agen.",
    "CRM berupa pengelolaan prospek dan kontak calon siswa dengan skor prioritas yang rinciannya dapat dilihat.",
    "Mesin anti-ban berupa batas laju bertingkat, jeda pengiriman, antrean keluar, dan pusat risiko.",
    "Dashboard pemantauan per nomor: volume percakapan, waktu balas pertama, percakapan belum dibalas, dan konversi.",
    "Pengelolaan tim dan hak akses serta log audit atas setiap tindakan penting.",
])
add("p", "Penjelasan rinci setiap fitur ditulis pada Bab III.")

add("h2", "2.3 Karakteristik Pengguna")
add("p", "Pengguna SAPA terbagi menjadi empat jenis seperti pada {tab:pengguna}.")
add("table", "pengguna", "Karakteristik Pengguna", ["Jenis pengguna", "Tanggung jawab dan hak akses", "Tingkat keahlian"], [
    ["Agen/CS", "Admin dan sales Asentra. Membalas percakapan serta mengelola prospek dan kontak, hanya pada nomor "
     "WhatsApp yang ditugaskan.", "Pemula sampai menengah; terbiasa memakai WhatsApp"],
    ["Supervisor", "Pengelola Asentra yang memantau kinerja layanan. Membaca semua nomor, mengelola basis pengetahuan, "
     "dan membaca log audit.", "Menengah"],
    ["Administrator", "Pengelola sistem. Mengakses seluruh fitur, termasuk nomor WhatsApp, pengaturan AI dan anti-ban, "
     "serta tim dan akses.", "Menengah sampai mahir"],
    ["Pelanggan", "Calon siswa atau orang tua yang menghubungi nomor WhatsApp Asentra. Tidak login ke SAPA.",
     "Pengguna umum WhatsApp"],
], [3.0, 8.0, 4.0])

add("h2", "2.4 Lingkungan Operasi")
add("p", "SAPA dijalankan pada lingkungan perangkat keras dan perangkat lunak seperti pada {tab:lingkungan}.")
add("table", "lingkungan", "Lingkungan Operasi Sistem", ["Komponen", "Spesifikasi"], [
    ["Server", "VPS 2 vCPU (AMD EPYC 9754), RAM 2 GB (+ swap 2 GB), SSD 40 GB, Ubuntu 24.04 LTS (x86_64)"],
    ["Web server", "Nginx dengan PHP-FPM 8.2"],
    ["Aplikasi", "Laravel 12 (PHP 8.2), Blade, Tailwind CSS 4, Vite 7; queue worker dan scheduler Laravel untuk antrean "
     "pesan keluar"],
    ["WA Gateway", "Node.js 22 LTS dengan pustaka @whiskeysockets/baileys versi 6"],
    ["Basis data", "SQLite 3 dengan modul FTS5 untuk pencarian teks penuh"],
    ["Peramban", "Google Chrome atau Microsoft Edge versi terbaru"],
    ["Perangkat klien", "Laptop atau PC dengan resolusi minimal 1366 × 768; ponsel Android dengan WhatsApp dan kamera "
     "untuk memindai QR (pengujian memakai ponsel Android 15)"],
    ["Jaringan", "Koneksi internet lebih dari 10 Mbps untuk sesi WhatsApp Web dan pemanggilan API AI"],
], [3.5, 11.5])

add("h2", "2.5 Batasan Desain dan Implementasi")
add("p", "Batasan yang harus dipatuhi selama perancangan dan implementasi adalah sebagai berikut.")
add("ol", [
    "**Framework.** Aplikasi dibangun dengan Laravel 12 dan pola MVC. Keputusan ini diambil tim pada 6 November 2026 "
    "dan disetujui dosen pengampu, menggantikan rencana awal Node.js, Express, dan React pada laporan ASN1.",
    "**Gateway terpisah.** Baileys hanya berjalan pada Node.js, sehingga WA Gateway dijalankan sebagai layanan "
    "tersendiri dan hanya dapat dipanggil dari server yang sama.",
    "**Kanal tidak resmi.** SAPA memakai WhatsApp Web, bukan WhatsApp Business API, sehingga risiko pembatasan nomor "
    "dikendalikan melalui mesin anti-ban.",
    "**Akses melalui peramban.** Sistem hanya diakses melalui peramban web dengan antarmuka berbahasa Indonesia.",
    "**Waktu.** Pengembangan berlangsung tiga sprint (enam minggu), dimulai 9 November 2026 dengan demo akhir kepada "
    "mitra pada 18 Desember 2026.",
    "**Kapasitas tim.** Lima anggota dengan 4 jam produktif per hari, setara 33 Story Point per sprint.",
    "**Data uji.** Basis data dimulai kosong tanpa data contoh, dan pengujian memakai nomor WhatsApp cadangan, bukan "
    "nomor operasional mitra.",
    "**Keamanan data.** Password disimpan sebagai hash bcrypt bawaan Laravel, dan kunci API penyedia AI disimpan "
    "terenkripsi memakai fitur enkripsi Laravel (AES-256 dengan APP_KEY).",
])

add("h2", "2.6 Asumsi dan Ketergantungan")
add("p", "Keberhasilan sistem bergantung pada asumsi sebagai berikut.")
add("ol", [
    "Mitra menyediakan dan memeriksa isi katalog program (jenjang, mata pelajaran, durasi, kapasitas kelas, jadwal, "
    "biaya) serta artikel basis pengetahuan (jam operasional, fasilitas, cara pendaftaran, program persiapan tes).",
    "Administrator dapat memegang ponsel yang menyimpan nomor WhatsApp yang akan ditautkan.",
    "Koneksi internet stabil, dan layanan WhatsApp Web serta penyedia AI tetap tersedia. Apabila penyedia AI gagal, "
    "sistem beralih ke mode aturan bawaan.",
    "Pustaka Baileys tetap kompatibel dengan protokol WhatsApp Web selama masa proyek.",
    "Pemilik Asentra hadir pada Sprint Review, dan perubahan kebutuhan disampaikan melalui Product Owner.",
    "Estimasi Story Point bersifat awal dan dinilai ulang saat Sprint Planning.",
])

add("h2", "2.7 Dokumentasi Pengguna")
add("p", "Dokumentasi yang diserahkan bersama sistem adalah sebagai berikut.")
add("ul", [
    "Panduan pengguna (user manual) untuk Agen/CS, Supervisor, dan Administrator.",
    "Panduan instalasi pada README repositori GitHub, termasuk cara menjalankan WA Gateway.",
    "Dokumen SRS ini beserta berkas Visual Paradigm (SAPA.vpp) dan mockup Figma.",
    "Laporan akhir Capstone Project.",
])
add("p", "Penyusunan dokumentasi final dijadwalkan pada Sprint 3 (US17).")

# ====================================================================== BAB III
add("h1", "BAB III", "KEBUTUHAN SISTEM", "3")
add("h2", "3.1 Kebutuhan Fungsional")
add("p", "Kebutuhan fungsional menjelaskan apa yang harus dapat dilakukan oleh sistem. Setiap kebutuhan diberi kode unik "
         "agar dapat ditelusuri sampai tahap pengujian. Prioritas ditentukan dengan metode MoSCoW, yaitu Must have "
         "(wajib), Should have (penting), Could have (bagus apabila ada), dan Won't have (tidak dikerjakan pada rilis "
         "ini). Daftar kebutuhan fungsional ditunjukkan pada {tab:fr}.")
add("table", "fr", "Daftar Kebutuhan Fungsional", ["Kode", "Kebutuhan fungsional", "Aktor", "Prioritas"], [
    ["F01", "Sistem menyediakan login dengan email dan password, lalu mengarahkan pengguna ke halaman awal sesuai role.",
     "Agen/CS, Supervisor, Administrator", "Must"],
    ["F02", "Sistem menerima pesan dari semua nomor WhatsApp yang tertaut dan menyimpannya dalam satu basis data.",
     "Pelanggan, WhatsApp Web", "Must"],
    ["F03", "Sistem membuat kontak dan prospek untuk nomor pengirim baru, serta mengisi jenjang, kelas, dan mata "
     "pelajaran dari isi percakapan.", "Sistem", "Must"],
    ["F04", "Sistem menjawab otomatis dari basis pengetahuan disertai sumber dan nilai keyakinan.", "Sistem, Penyedia AI",
     "Must"],
    ["F05", "Sistem mengalihkan percakapan ke agen apabila keyakinan rendah, terdapat kata kunci eskalasi, atau nada "
     "pesan marah.", "Sistem, Agen/CS", "Must"],
    ["F06", "Sistem menilai setiap pesan keluar dengan mesin anti-ban (kirim, tunda, atau tahan) serta mengelola antrean "
     "keluar dan pusat risiko.", "Sistem, Administrator", "Must"],
    ["F07", "Agen membaca, membalas, mengambil alih, dan menyelesaikan percakapan pada nomor yang diizinkan.", "Agen/CS",
     "Must"],
    ["F08", "Agen mengelola tahap prospek, catatan aktivitas, dan jadwal tindak lanjut; skor prioritas tampil beserta "
     "rinciannya.", "Agen/CS", "Must"],
    ["F09", "Agen mencari dan memperbarui data kontak calon siswa.", "Agen/CS", "Could"],
    ["F10", "Sistem menampilkan dashboard per nomor: volume percakapan, waktu balas pertama, percakapan belum dibalas, "
     "dan konversi.", "Supervisor, Administrator", "Should"],
    ["F11", "Administrator menautkan, memantau, dan memutus nomor WhatsApp melalui kode QR.", "Administrator", "Must"],
    ["F12", "Supervisor atau Administrator mengelola dan menguji artikel basis pengetahuan.", "Supervisor, Administrator",
     "Must"],
    ["F13", "Administrator mengatur penyedia AI, ambang keyakinan, kata kunci eskalasi, dan batas anti-ban, serta menguji "
     "keputusan AI.", "Administrator", "Should"],
    ["F14", "Administrator mengelola pengguna, role, dan akses per nomor WhatsApp.", "Administrator", "Should"],
    ["F15", "Sistem mencatat log audit setiap tindakan penting dan menampilkannya dengan filter.",
     "Supervisor, Administrator", "Should"],
    ["W01", "Verifikasi login dua faktor (2FA) dengan kode OTP.", "Agen/CS, Supervisor, Administrator", "Won't"],
    ["W02", "Pengiriman pesan promosi massal (broadcast) ke daftar kontak.", "Administrator", "Won't"],
    ["W03", "Kanal selain WhatsApp, misalnya Instagram, Telegram, atau email.", "Pelanggan", "Won't"],
    ["W04", "Integrasi WhatsApp Business API resmi.", "Administrator", "Won't"],
    ["W05", "Aplikasi mobile native untuk Agen/CS.", "Agen/CS", "Won't"],
], [1.3, 8.7, 3.4, 1.6])
add("p", "Kode F01 sampai F15 setara dengan FR-01 sampai FR-15 pada laporan ASN1. Prioritas Must, Should, dan Could "
         "diturunkan dari prioritas Tinggi, Sedang, dan Rendah pada Product Backlog. Butir W01 (2FA) tidak dikerjakan "
         "karena SAPA hanya dipakai oleh empat sampai lima staf internal mitra, sedangkan risiko akses tidak sah "
         "ditekan dengan pembatasan percobaan login, akses per nomor, dan log audit. Butir W01 sampai W05 dapat "
         "dipertimbangkan pada rilis berikutnya.")
add("p", "Setiap kebutuhan fungsional berprioritas Must, Should, dan Could dirinci dengan format pada {tab:f01} sampai "
         "{tab:f15}.")

FD = [  # (kunci, kode, nama, deskripsi, aktor, prakondisi, alur normal, alur alternatif, pascakondisi, kriteria)
    ("f01", "F01", "Login Pengguna",
     "Pengguna memasukkan email dan password untuk masuk ke SAPA sesuai role dan nomor WhatsApp yang menjadi aksesnya.",
     "Agen/CS, Supervisor, Administrator",
     "Pengguna memiliki akun aktif yang dibuat Administrator dan berada di halaman Login.",
     ["Pengguna membuka halaman Login.", "Sistem menampilkan form email dan password.",
      "Pengguna mengisi email dan password, lalu menekan \"Masuk\".", "Sistem memvalidasi kredensial.",
      "Sistem mengambil role dan daftar nomor WhatsApp yang boleh diakses.",
      "Sistem mencatat log audit login dan menampilkan halaman awal sesuai role (Dashboard untuk Supervisor dan "
      "Administrator, Kotak Masuk untuk Agen/CS)."],
     "4a. Akun nonaktif: sistem menampilkan \"Akun Anda dinonaktifkan, hubungi Administrator\".\n"
     "4b. Email atau password salah: sistem menampilkan \"Email atau password salah\"; setelah lima kali gagal "
     "berturut-turut, login ditahan 5 menit.",
     "Pengguna masuk, sesi aktif, dan menu yang tampil sesuai role.",
     "Login berhasil dengan data valid; ditolak dengan data tidak valid; akun nonaktif ditolak; login ditahan 5 menit "
     "setelah lima kali gagal."),
    ("f02", "F02", "Menerima Pesan WhatsApp",
     "Sistem menerima pesan pelanggan dari nomor WhatsApp Asentra yang tertaut, lalu menyimpan pesan dan percakapannya.",
     "Pelanggan, WhatsApp Web", "Nomor WhatsApp Asentra yang dituju berstatus tersambung.",
     ["Pelanggan mengirim pesan ke nomor WhatsApp Asentra.",
      "WA Gateway menerima pesan dan meneruskannya ke Laravel melalui webhook HTTP lokal.",
      "Sistem mencari kontak berdasarkan nomor pengirim; apabila belum ada, sistem membuat kontak dan prospek baru (F03).",
      "Sistem membuka atau memperbarui percakapan dan menyimpan pesan.", "Sistem menjalankan jawaban otomatis (F04)."],
     "5a. Percakapan sedang ditangani agen: sistem tidak memanggil AI, menandai percakapan \"belum dibalas\", dan "
     "memberi tanda pada Kotak Masuk.\nGalat: nomor tujuan terputus, pesan tidak diterima dan status nomor tampil "
     "\"terputus\" pada halaman Nomor WhatsApp.",
     "Pesan tersimpan dan percakapan tampil di Kotak Masuk.",
     "Pesan dari setiap nomor tertaut tampil di Kotak Masuk; percakapan yang ditangani agen tidak dijawab AI; status "
     "nomor terputus tampil dengan benar."),
    ("f03", "F03", "Kontak dan Prospek Otomatis",
     "Sistem membuat kontak dan prospek bagi pengirim baru, lalu memperbarui jenjang, kelas, dan mata pelajaran dari "
     "isi percakapan.", "Sistem", "Pesan masuk telah tersimpan (F02).",
     ["Sistem mencari kontak berdasarkan nomor pengirim.",
      "Apabila belum ada, sistem membuat kontak baru dan prospek bertahap \"baru\".",
      "Sistem mengklasifikasi maksud pesan dan mengekstrak entitas (nama, jenjang, kelas, mata pelajaran).",
      "Sistem memperbarui data kontak dan menghitung ulang skor prioritas prospek."],
     "2a. Kontak sudah ada: sistem hanya memperbarui data yang berubah.",
     "Kontak dan prospek tercatat dan data calon siswa terisi dari percakapan.",
     "Pengirim baru otomatis menjadi kontak dan prospek tahap \"baru\"; jenjang, kelas, dan mata pelajaran terisi tanpa "
     "input manual; skor prioritas diperbarui."),
    ("f04", "F04", "Jawaban Otomatis AI",
     "Sistem mencari jawaban di basis pengetahuan, menyusun jawaban, menghitung keyakinan, lalu mengirim jawaban "
     "beserta sumber.", "Sistem, Penyedia AI", "Pesan masuk telah tersimpan dan mode AI aktif untuk nomor tersebut.",
     ["Sistem mencari artikel basis pengetahuan yang relevan dengan FTS5.",
      "Penyedia AI menyusun jawaban dari artikel terpilih.",
      "Sistem menghitung nilai keyakinan dan membandingkannya dengan ambang (F05).",
      "Sistem menilai pesan keluar dengan mesin anti-ban dan memasukkannya ke antrean keluar (F06).",
      "WA Gateway mengirim balasan beserta sumber.", "Sistem mencatat jejak keputusan AI dan metrik harian."],
     "Galat: penyedia AI gagal atau timeout, sistem beralih ke mode aturan bawaan; tidak ada artikel relevan, "
     "percakapan dialihkan ke agen.",
     "Balasan bersumber terkirim atau percakapan dialihkan ke agen; jejak keputusan AI tersimpan.",
     "Setiap jawaban AI menyertakan sumber dan nilai keyakinan; pertanyaan tanpa artikel relevan dialihkan ke agen; laju "
     "halusinasi kurang dari 5% pada 50 pertanyaan uji (target pengukuran)."),
    ("f05", "F05", "Eskalasi ke Agen",
     "Sistem mengalihkan percakapan dari AI ke agen ketika AI tidak yakin atau pelanggan perlu ditangani manusia.",
     "Sistem, Agen/CS", "AI sedang memproses pesan pelanggan (F04).",
     ["Sistem menghitung nilai keyakinan jawaban.",
      "Sistem membandingkan nilai dengan ambang keyakinan serta memeriksa kata kunci eskalasi dan nada pesan.",
      "Apabila salah satu syarat eskalasi terpenuhi, sistem mengalihkan percakapan ke agen dan menghentikan AI.",
      "Sistem mengirim pesan \"Pertanyaan Anda kami teruskan ke admin\"."],
     "3a. Tidak ada syarat eskalasi yang terpenuhi: jawaban AI dikirim seperti biasa (F04).",
     "Percakapan berstatus ditangani agen dan AI berhenti membalas.",
     "Eskalasi terjadi saat keyakinan di bawah ambang, terdapat kata kunci (misalnya \"admin\" atau \"komplain\"), atau "
     "nada marah; setelah eskalasi AI tidak membalas lagi."),
    ("f06", "F06", "Mesin Anti-ban",
     "Sistem menilai setiap pesan keluar sebelum dikirim agar ritme pengiriman menyerupai manusia dan risiko "
     "pembatasan nomor berkurang.", "Sistem, Administrator", "Terdapat pesan keluar dari AI atau agen.",
     ["Sistem menilai pesan berdasarkan batas laju per menit, per jam, dan per hari, jeda minimum dan maksimum, serta "
      "jam aktif.", "Sistem memberi keputusan kirim, tunda, atau tahan.",
      "Pesan berkeputusan \"kirim\" masuk antrean keluar dan dikirim queue worker dengan jeda.",
      "Sistem mencatat pesan yang ditunda atau ditahan serta insidennya di Pusat Risiko."],
     "Galat: pesan agen yang ditahan menampilkan \"Pesan ditunda oleh pengaman pengiriman\".",
     "Pesan terkirim sesuai ritme aman atau tersimpan di antrean; insiden tercatat.",
     "Pesan yang melebihi batas tidak langsung terkirim; antrean tetap tersimpan apabila nomor terputus; insiden tampil "
     "di Pusat Risiko."),
    ("f07", "F07", "Mengelola Percakapan",
     "Agen melihat percakapan dari nomor yang menjadi tanggung jawabnya, membaca jawaban AI beserta sumbernya, lalu "
     "membalas, mengambil alih, atau menyelesaikan percakapan.", "Agen/CS",
     "Agen telah login (F01) dan memiliki akses minimal satu nomor WhatsApp.",
     ["Agen memilih menu Kotak Masuk.",
      "Sistem menampilkan percakapan dari nomor yang diizinkan, diurutkan dari yang belum dibalas.",
      "Agen memilih percakapan; sistem menampilkan riwayat pesan, jawaban AI dan sumbernya, data pelanggan, dan jejak "
      "keputusan AI.", "Agen menekan \"Ambil alih\", mengetik balasan, lalu menekan \"Kirim\".",
      "Sistem menghentikan AI untuk percakapan ini, menilai pesan dengan anti-ban, dan mengirim balasan.",
      "Sistem memperbarui status, metrik waktu balas pertama, dan log audit."],
     "4a. Agen menekan \"Selesaikan\": status percakapan menjadi selesai.\n4b. Agen menekan \"Kembalikan ke AI\": "
     "balasan AI aktif kembali.\nGalat: membuka percakapan nomor yang tidak diizinkan ditolak dengan \"Anda tidak "
     "memiliki akses ke nomor ini\".",
     "Balasan terkirim, status dan metrik waktu balas diperbarui, log audit tercatat.",
     "Agen hanya melihat percakapan pada nomor yang diizinkan; ambil alih menghentikan AI; tombol Selesaikan dan "
     "Kembalikan ke AI mengubah status dengan benar."),
    ("f08", "F08", "Mengelola Prospek",
     "Agen memantau calon siswa per tahap, melihat skor prioritas beserta rinciannya, memindahkan tahap, dan mencatat "
     "aktivitas tindak lanjut.", "Agen/CS", "Agen telah login (F01) dan terdapat prospek pada nomor yang diizinkan.",
     ["Agen memilih menu Prospek.", "Sistem menampilkan papan prospek per tahap, diurutkan berdasarkan skor prioritas.",
      "Agen memilih kartu prospek; sistem menampilkan detail, rincian lima komponen skor, riwayat aktivitas, dan link "
      "ke percakapan.", "Agen mengubah tahap, menambah catatan, dan menetapkan tanggal tindak lanjut, lalu menekan "
      "\"Simpan\".", "Sistem menyimpan perubahan, menghitung ulang skor, dan mencatat log audit."],
     "4a. Prospek dipindah ke tahap \"daftar\": sistem menambah hitungan konversi pada metrik harian.\nGalat: catatan "
     "kosong ditolak dengan \"Catatan wajib diisi\".",
     "Tahap prospek, catatan aktivitas, dan jadwal tindak lanjut tersimpan.",
     "Prospek tampil per tahap dengan skor dan rinciannya; perpindahan tahap tersimpan; konversi bertambah saat prospek "
     "berstatus \"daftar\"."),
    ("f09", "F09", "Mengelola Kontak",
     "Agen mencari dan memperbarui data kontak calon siswa (nama, jenjang, kelas, mata pelajaran, kota, sumber, label).",
     "Agen/CS", "Agen telah login (F01).",
     ["Agen memilih menu Kontak dan mengetik kata kunci.", "Sistem menampilkan daftar kontak yang sesuai.",
      "Agen memilih kontak lalu menekan \"Ubah\"; sistem menampilkan form data beserta riwayat percakapan.",
      "Agen memperbarui data dan menekan \"Simpan\".", "Sistem memvalidasi, menyimpan perubahan, dan mencatat log audit."],
     "2a. Kontak tidak ditemukan: sistem menampilkan \"Kontak tidak ditemukan\".\nGalat: format nomor tidak valid atau "
     "sudah terdaftar ditolak dan kolom yang salah ditandai.",
     "Data kontak terbaru tersimpan dan dipakai oleh AI serta skor prospek.",
     "Pencarian menemukan kontak sesuai kata kunci; perubahan tersimpan; nomor tidak valid atau duplikat ditolak."),
    ("f10", "F10", "Dashboard Pemantauan",
     "Pengguna memantau kinerja layanan per nomor WhatsApp: volume percakapan, waktu balas pertama, percakapan belum "
     "dibalas, balasan AI dan agen, serta konversi.", "Supervisor, Administrator",
     "Pengguna telah login (F01) sebagai Supervisor atau Administrator.",
     ["Pengguna memilih menu Dashboard.",
      "Sistem mengambil metrik harian seluruh nomor yang diizinkan dan menampilkan kartu ringkasan, grafik volume, dan "
      "status tiap nomor.", "Pengguna memilih filter nomor dan periode.",
      "Sistem menghitung ulang metrik sesuai filter dan menampilkan hasilnya."],
     "3a. Pengguna memilih nomor tertentu atau periode (hari ini, 7 hari, 30 hari); grafik diperbarui.\nGalat: tidak "
     "ada data pada periode terpilih, sistem menampilkan \"Belum ada data pada periode ini\".",
     "Pengguna memperoleh ringkasan kinerja layanan sesuai filter.",
     "Dashboard menampilkan empat metrik utama per nomor; filter nomor dan periode mengubah tampilan; kondisi tanpa "
     "data ditangani."),
    ("f11", "F11", "Mengelola Nomor WhatsApp",
     "Administrator menambah nomor WhatsApp (label, nomor, tujuan admin atau sales), menautkannya dengan memindai QR, "
     "memantau status sesi, dan memutus nomor.", "Administrator",
     "Administrator telah login (F01) dan memegang ponsel dengan nomor yang akan ditautkan.",
     ["Administrator memilih menu Nomor WhatsApp dan menekan \"Tambah Nomor\".",
      "Sistem menampilkan form label, nomor, dan tujuan nomor.", "Administrator mengisi form dan menekan \"Tautkan\".",
      "Sistem meminta WA Gateway membuat sesi WhatsApp Web dan menampilkan kode QR.",
      "Administrator memindai QR dari aplikasi WhatsApp di ponsel.",
      "Sistem menerima konfirmasi tertaut, menyimpan sesi, mengubah status menjadi tersambung, dan mencatat log audit."],
     "6a. Administrator menekan \"Putuskan\": sesi berakhir dan status menjadi terputus.\nGalat: QR kedaluwarsa "
     "(sekitar 60 detik) menampilkan \"QR kedaluwarsa\" dan tombol \"Buat ulang QR\"; penautan gagal berstatus \"gagal "
     "tertaut\" dan dicatat di Pusat Risiko.",
     "Nomor berstatus tersambung dan pesannya masuk ke Kotak Masuk.",
     "Nomor tertaut setelah QR dipindai; QR kedaluwarsa dapat dibuat ulang; pemutusan mengubah status; satu nomor "
     "terputus tidak memengaruhi nomor lain."),
    ("f12", "F12", "Mengelola Basis Pengetahuan",
     "Pengguna menambah, mengubah, menonaktifkan, dan menguji artikel basis pengetahuan yang menjadi sumber jawaban AI.",
     "Supervisor, Administrator", "Pengguna telah login (F01) sebagai Supervisor atau Administrator.",
     ["Pengguna memilih menu Basis Pengetahuan; sistem menampilkan daftar artikel per kategori.",
      "Pengguna menekan \"Tambah Artikel\" atau memilih artikel.",
      "Sistem menampilkan form judul, kategori, isi, label, dan status aktif.", "Pengguna mengisi form dan menekan "
      "\"Simpan\".", "Sistem memvalidasi, menyimpan artikel, mengindeks ulang FTS5, dan mencatat log audit."],
     "4a. Pengguna menekan \"Uji Pencarian\" dan mengetik pertanyaan; sistem menampilkan artikel paling relevan beserta "
     "skornya.\nGalat: judul atau isi kosong ditolak dengan \"Judul dan isi wajib diisi\".",
     "Artikel tersimpan dan terindeks ulang sehingga langsung dipakai AI.",
     "Artikel dapat ditambah, diubah, dan dinonaktifkan; artikel baru langsung ditemukan oleh pencarian; judul atau isi "
     "kosong ditolak."),
    ("f13", "F13", "Mengatur AI dan Anti-ban",
     "Administrator mengatur penyedia AI, kunci API, persona, ambang keyakinan, kata kunci eskalasi, dan batas "
     "pengiriman anti-ban, serta menguji keputusan AI di konsol uji.", "Administrator", "Administrator telah login (F01).",
     ["Administrator memilih menu Pengaturan AI; sistem menampilkan pengaturan AI dan anti-ban yang berlaku.",
      "Administrator mengubah penyedia AI, kunci API, ambang keyakinan, kata kunci eskalasi, dan batas pengiriman, lalu "
      "menekan \"Simpan\".", "Sistem memvalidasi nilai dan menguji koneksi penyedia AI.",
      "Sistem mengenkripsi kunci API, menyimpan pengaturan, dan mencatat log audit."],
     "3a. Administrator menekan \"Uji Keputusan\" dan memasukkan contoh pesan; sistem menampilkan jejak keputusan "
     "(maksud, entitas, artikel, keyakinan, keputusan kirim atau eskalasi).\nGalat: kunci API ditolak penyedia "
     "menampilkan \"Kunci API ditolak penyedia\" dan pengaturan lama tetap dipakai; nilai batas yang tidak wajar ditolak.",
     "Pengaturan baru tersimpan dan berlaku untuk pesan berikutnya.",
     "Pengaturan berlaku pada pesan berikutnya; kunci API tersimpan terenkripsi; konsol uji menampilkan jejak "
     "keputusan; nilai tidak wajar ditolak."),
    ("f14", "F14", "Mengelola Tim dan Hak Akses",
     "Administrator menambah pengguna, menetapkan role, mengatur level akses per nomor WhatsApp, dan menonaktifkan "
     "pengguna.", "Administrator", "Administrator telah login (F01).",
     ["Administrator memilih menu Tim & Akses; sistem menampilkan daftar pengguna, role, dan akses nomor.",
      "Administrator menekan \"Tambah Pengguna\" atau memilih pengguna.",
      "Sistem menampilkan form nama, email, role, dan matriks akses per nomor.",
      "Administrator mengisi form, memilih level akses tiap nomor, lalu menekan \"Simpan\".",
      "Sistem memvalidasi, menyimpan pengguna dan akses nomor, serta mencatat log audit."],
     "4a. Administrator menekan \"Nonaktifkan\": status pengguna berubah dan sesinya berakhir.\nGalat: email yang sudah "
     "terdaftar ditolak dengan \"Email sudah digunakan\"; Administrator tidak dapat menonaktifkan dirinya sendiri.",
     "Akun dan hak akses tersimpan dan langsung berlaku pada permintaan berikutnya.",
     "Pengguna baru dapat login sesuai role dan akses nomor; perubahan akses langsung berlaku; email duplikat dan "
     "penonaktifan diri sendiri ditolak."),
    ("f15", "F15", "Melihat Log Audit",
     "Pengguna menelusuri riwayat tindakan penting (login, perubahan pengaturan, ambil alih, perubahan akses) "
     "berdasarkan pelaku, jenis aksi, dan rentang tanggal.", "Supervisor, Administrator",
     "Pengguna telah login (F01) sebagai Supervisor atau Administrator.",
     ["Pengguna memilih menu Log Audit; sistem menampilkan log terbaru.",
      "Pengguna mengisi filter pelaku, jenis aksi, dan rentang tanggal.",
      "Sistem mengambil dan menampilkan log sesuai filter."],
     "3a. Pengguna memilih satu baris log; sistem menampilkan detail perubahan.\nGalat: tidak ada log sesuai filter, "
     "sistem menampilkan \"Tidak ada aktivitas pada filter ini\".",
     "Pengguna memperoleh daftar log yang sesuai filter.",
     "Tindakan penting tercatat dan dapat difilter; detail perubahan dapat dibuka; kondisi tanpa hasil ditangani."),
]
for key, kode, nama, desk, aktor, pra, alur, alt, pasca, kriteria in FD:
    add("kv", key, f"Rincian Kebutuhan Fungsional {kode}", [
        ["Kode / Nama", f"{kode}: {nama}"], ["Deskripsi", desk], ["Aktor", aktor], ["Prakondisi", pra],
        ["Alur normal", "\n".join(f"{i}. {s}" for i, s in enumerate(alur, 1))], ["Alur alternatif", alt],
        ["Pascakondisi", pasca], ["Kriteria penerimaan", kriteria]])

add("h2", "3.2 Kebutuhan Non-Fungsional")
add("p", "Kebutuhan non-fungsional menggambarkan seberapa baik sistem harus bekerja. Setiap kebutuhan dirumuskan dengan "
         "angka atau cara uji yang jelas agar dapat dibuktikan pada tahap pengujian, seperti pada {tab:nfr}.")
add("table", "nfr", "Kebutuhan Non-Fungsional", ["Kode", "Kategori", "Kebutuhan", "Cara mengukur"], [
    ["NF01", "Performa", "Halaman Kotak Masuk dengan 500 percakapan tampil kurang dari 3 detik pada koneksi 10 Mbps.",
     "Pengukuran waktu muat halaman di Chrome DevTools"],
    ["NF02", "Performa", "Balasan otomatis masuk antrean kurang dari 5 detik untuk 90% pesan, di luar waktu pemanggilan "
     "model AI dan jeda anti-ban.", "Selisih waktu pesan masuk dan pesan masuk antrean pada log uji"],
    ["NF03", "Keamanan", "Hak akses per nomor ditegakkan di server melalui middleware pada setiap permintaan.",
     "Uji akses ke nomor yang tidak diizinkan harus ditolak (HTTP 403)"],
    ["NF04", "Keamanan", "Password disimpan sebagai hash bcrypt; kunci API disimpan terenkripsi; tidak ada kredensial "
     "di repositori.", "Pemeriksaan basis data dan tinjauan kode"],
    ["NF05", "Keamanan", "Seluruh akses peramban memakai HTTPS; sesi berakhir setelah 120 menit tanpa aktivitas.",
     "Pemeriksaan sertifikat dan uji sesi"],
    ["NF06", "Keandalan", "Satu nomor yang terputus tidak menghentikan nomor lain; antrean pesan keluar tetap tersimpan "
     "saat WA Gateway dimulai ulang.", "Uji pemutusan satu nomor dan restart gateway"],
    ["NF07", "Keandalan", "Basis data dicadangkan otomatis setiap hari dan backup disimpan 7 hari.",
     "Pemeriksaan jadwal scheduler dan berkas backup"],
    ["NF08", "Ketersediaan", "Aplikasi dan WA Gateway berjalan 24 jam pada VPS; target persentase ketersediaan "
     "ditetapkan bersama mitra.", "Monitoring uptime"],
    ["NF09", "Kepatuhan kanal", "Tidak ada pesan promosi massal; bot hanya membalas percakapan yang dimulai pelanggan.",
     "Tinjauan alur pengiriman dan uji antrean keluar"],
    ["NF10", "Kemudahan penggunaan", "Antarmuka berbahasa Indonesia; skor System Usability Scale (SUS) minimal 68 pada "
     "UAT bersama admin dan sales mitra.", "Kuesioner SUS saat UAT"],
    ["NF11", "Kepatuhan hukum", "Data pribadi calon siswa diproses seperlunya dengan akses terbatas sesuai UU Nomor 27 "
     "Tahun 2022 (Republik Indonesia, 2022).", "Checklist kepatuhan"],
    ["NF12", "Akurasi AI", "Setiap jawaban AI menyertakan sumber; laju halusinasi kurang dari 5% pada 50 pertanyaan uji.",
     "Pengujian 50 pertanyaan terhadap basis pengetahuan"],
    ["NF13", "Auditabilitas", "Setiap tindakan penting tercatat pada log audit yang tidak dapat diubah dari antarmuka.",
     "Pemeriksaan log setelah setiap skenario uji"],
    ["NF14", "Pemeliharaan", "Kode mengikuti konvensi Laravel (Laravel Pint) dan setiap perubahan masuk melalui pull "
     "request yang ditinjau anggota lain.", "Riwayat pull request di GitHub"],
], [1.3, 2.6, 6.6, 4.5])
add("p", "Target NF08 dan NF10 masih perlu dikonfirmasi dengan mitra dan dicatat pada Lampiran C.")

add("h2", "3.3 Kebutuhan Antarmuka Eksternal")
add("h3", "3.3.1 Antarmuka Pengguna")
add("p", "Antarmuka berupa aplikasi web yang disusun dengan Blade dan Tailwind CSS, berbahasa Indonesia, dan "
         "menyesuaikan ukuran layar. Menu samping hanya menampilkan menu yang sesuai role pengguna. Tampilan mengikuti "
         "panduan gaya pada {tab:gaya}, dan rancangan sebelas halaman utama ditampilkan pada Bab V.")
add("h3", "3.3.2 Antarmuka Perangkat Keras")
add("p", "Sistem tidak memerlukan perangkat keras khusus seperti printer atau barcode scanner. Perangkat yang terlibat "
         "adalah ponsel Android dengan aplikasi WhatsApp dan kamera, yang dipakai Administrator untuk memindai kode QR "
         "saat menautkan nomor.")
add("h3", "3.3.3 Antarmuka Perangkat Lunak")
add("p", "Sistem berinteraksi dengan perangkat lunak dan layanan lain seperti pada {tab:antarmukasw}.")
add("table", "antarmukasw", "Antarmuka Perangkat Lunak", ["Sistem atau layanan", "Data yang dikirim SAPA",
                                                          "Data yang diterima SAPA"], [
    ["WA Gateway (Node.js, Baileys)", "Perintah buat sesi, putus sesi, dan kirim pesan (nomor tujuan, isi)",
     "Kode QR, status sesi, pesan masuk (nomor pengirim, isi, waktu), status terkirim"],
    ["Penyedia AI (OpenAI, kompatibel OpenAI, atau Gemini)", "Pesan pelanggan, artikel basis pengetahuan terpilih, "
     "instruksi persona", "Klasifikasi maksud, entitas, dan jawaban yang disusun"],
    ["SQLite dengan FTS5", "Data aplikasi dan query pencarian artikel", "Hasil query dan peringkat artikel (bm25)"],
], [4.5, 5.25, 5.25])
add("h3", "3.3.4 Antarmuka Komunikasi")
add("p", "Jalur komunikasi antarkomponen sistem adalah sebagai berikut.")
add("ol", [
    "**Peramban ke Laravel.** HTTPS dengan form Blade dan permintaan AJAX berformat JSON.",
    "**Laravel ke WA Gateway.** HTTP lokal (localhost) berformat JSON dengan token rahasia bersama pada header. Pesan "
    "masuk diteruskan WA Gateway ke webhook Laravel, sedangkan pesan keluar dikirim queue worker Laravel ke endpoint "
    "kirim pada WA Gateway.",
    "**WA Gateway ke WhatsApp.** Sesi WhatsApp Web melalui WebSocket yang dikelola Baileys. Kode QR penautan kedaluwarsa "
    "sekitar 60 detik.",
    "**Laravel ke penyedia AI.** HTTPS REST berformat JSON dengan kunci API yang didekripsi saat dipakai.",
])

add("h2", "3.4 Kebutuhan Data")
add("h3", "3.4.1 Kamus Data")
add("p", "Kamus data disusun dari ERD pada {fig:erd1} dan {fig:erd2}. Nama tabel dan kolom mengikuti konvensi Laravel "
         "(snake_case, kunci utama id, kunci tamu <tabel>_id). Setiap tabel juga memiliki kolom created_at dan "
         "updated_at bawaan Laravel yang tidak ditulis ulang pada {tab:kamus}.")
add("kamus", "kamus", "Kamus Data")
add("h3", "3.4.2 Aturan Bisnis dan Validasi Data")
add("p", "Aturan yang berlaku di Asentra dan harus dipatuhi sistem adalah sebagai berikut.")
add("ol", [
    "**BR01.** Login memakai email dan password; akun nonaktif tidak dapat masuk, dan setelah lima kali gagal "
    "berturut-turut login ditahan 5 menit.",
    "**BR02.** Email pengguna harus unik; Administrator tidak dapat menonaktifkan dirinya sendiri; penonaktifan "
    "mengakhiri sesi pengguna.",
    "**BR03.** Hak akses per nomor ditegakkan di server. Agen/CS hanya mengakses nomor yang ditugaskan, Supervisor "
    "membaca semua nomor, dan Administrator memiliki seluruh fitur.",
    "**BR04.** Nomor pengirim baru otomatis menjadi kontak dan prospek tahap \"baru\"; nomor WhatsApp kontak harus valid "
    "dan tidak boleh duplikat.",
    "**BR05.** Tahap prospek adalah baru, dihubungi, tertarik, penawaran, daftar, dan batal. Perpindahan ke \"daftar\" "
    "menambah hitungan konversi harian, dan catatan aktivitas wajib diisi.",
    "**BR06.** Skor prioritas dihitung dari lima komponen berbobot, dihitung ulang setiap data kontak atau tahap berubah, "
    "dan rinciannya dapat dilihat pengguna. Pendekatan skor yang transparan membantu tim penjualan mendahulukan "
    "prospek dengan peluang konversi tertinggi (González-Flores dkk., 2025).",
    "**BR07.** AI hanya menjawab dari artikel basis pengetahuan yang aktif dan selalu menyertakan sumber; tanpa artikel "
    "relevan, percakapan dialihkan ke agen.",
    "**BR08.** Setelah eskalasi atau ambil alih, AI berhenti membalas percakapan tersebut sampai agen menekan "
    "\"Kembalikan ke AI\".",
    "**BR09.** Setiap pesan keluar wajib dinilai mesin anti-ban sebelum dikirim; pesan yang ditunda atau ditahan tetap "
    "berada di antrean dan dicatat di Pusat Risiko.",
    "**BR10.** Bot hanya membalas percakapan yang dimulai pelanggan dan tidak mengirim pesan promosi massal.",
    "**BR11.** Kode QR kedaluwarsa sekitar 60 detik dan dapat dibuat ulang; kegagalan penautan dicatat di Pusat Risiko.",
    "**BR12.** Artikel basis pengetahuan wajib memiliki judul dan isi; setiap perubahan artikel memicu pengindeksan "
    "ulang FTS5.",
    "**BR13.** Nilai batas pengaturan tidak boleh negatif atau nol; kunci API yang ditolak penyedia tidak menggantikan "
    "pengaturan lama.",
    "**BR14.** Tindakan penting (login, perubahan pengaturan, ambil alih, perubahan akses, perubahan data kontak dan "
    "prospek) dicatat pada log audit.",
    "**BR15.** Data pribadi calon siswa dikelola seperlunya dengan akses terbatas; basis data dimulai kosong dan contoh "
    "percakapan pada dokumen dianonimkan.",
])

# ====================================================================== BAB IV
add("h1", "BAB IV", "MODEL ANALISIS SISTEM", "4")
add("p", "Bab ini menyajikan model sistem dalam bentuk diagram. Seluruh diagram dibuat dengan Visual Paradigm Community "
         "Edition memakai notasi UML, yang lazim dipakai pada perancangan sistem informasi untuk menggambarkan "
         "kebutuhan, alur, dan struktur sistem (Narulita dkk., 2024).")

add("h2", "4.1 Arsitektur Sistem")
add("p", "Arsitektur SAPA digambarkan dengan deployment diagram yang disusun berlapis, mengikuti model lapisan yang "
         "diberikan pada perkuliahan. Susunan lapisan dari bawah ke atas adalah sebagai berikut.")
add("ol", [
    "**Infrastruktur perangkat keras.** Server fisik milik penyedia VPS.",
    "**Virtual machine.** VPS Ubuntu 24.04 LTS dengan 2 vCPU, RAM 2 GB, dan SSD 40 GB.",
    "**Web server dan basis data.** Nginx dengan PHP-FPM 8.2, runtime Node.js 22 untuk WA Gateway, dan berkas SQLite.",
    "**OLTP dan OLAP.** Modul OLTP mencatat transaksi harian berupa pesan, percakapan, kontak, dan prospek. Modul OLAP "
    "merangkum metrik harian untuk dashboard.",
    "**Autentikasi.** Login dan RBAC per nomor. Lapisan 2FA pada model perkuliahan tidak diterapkan (W01).",
    "**Aplikasi.** Antarmuka web Blade yang dibuka melalui peramban.",
])
add("fig", "arsitektur", "Deployment Diagram Arsitektur SAPA", PNG + "Deployment Diagram Arsitektur SAPA.png",
    "Pada {fig:arsitektur}, pengguna membuka SAPA melalui HTTPS. Aplikasi Laravel memanggil WA Gateway melalui HTTP "
    "lokal, membaca dan menulis SQLite melalui PDO, dan memanggil penyedia AI melalui HTTPS REST. WA Gateway menjaga "
    "sesi WhatsApp Web untuk setiap nomor yang tertaut.")

add("h2", "4.2 Diagram Use Case")
add("p", "Use case diagram pada {fig:usecase} menggambarkan interaksi empat aktor utama (Pelanggan, Agen/CS, "
         "Supervisor, dan Administrator) serta dua aktor sekunder (WhatsApp Web dan Penyedia AI) dengan dua belas use "
         "case.")
add("fig", "usecase", "Use Case Diagram SAPA", PNG + "Use Case Diagram SAPA.png",
    "Setiap use case yang memerlukan autentikasi memiliki relasi <<Include>> ke Login. Use case Mengirim Pesan WhatsApp "
    "tidak memerlukan login karena dilakukan pelanggan melalui aplikasi WhatsApp, dan use case tersebut meng-include "
    "Menjawab Pesan Otomatis dengan AI.")
add("p", "Pemetaan use case ke kebutuhan fungsional ditunjukkan pada {tab:uc}.")
add("table", "uc", "Daftar Use Case", ["Nomor", "Use case", "Aktor", "Kebutuhan"],
    [list(u) for u in UC], [1.8, 5.4, 5.3, 2.5])

add("h2", "4.3 Diagram Aktivitas")
add("p", "Activity diagram diturunkan dari rincian kebutuhan fungsional pada Bab III. Swimlane kiri memuat aktivitas "
         "aktor dan swimlane kanan memuat aktivitas sistem, sedangkan percabangan menggambarkan alur alternatif dan "
         "kondisi galat. Activity diagram disusun untuk kedua belas use case pada {tab:uc}.")
AD_KET = {
    1: "Activity diagram Login menunjukkan validasi kredensial, penolakan akun nonaktif, dan pengalihan ke halaman "
       "awal sesuai role.",
    2: "Activity diagram Mengirim Pesan WhatsApp menunjukkan pembuatan kontak baru dan percabangan antara percakapan "
       "yang ditangani AI dan yang ditangani agen.",
    3: "Activity diagram Menjawab Pesan Otomatis dengan AI menunjukkan pencarian artikel, mode aturan bawaan saat "
       "penyedia AI gagal, eskalasi, dan penilaian anti-ban.",
    4: "Activity diagram Mengelola Percakapan menunjukkan pemeriksaan akses nomor, ambil alih oleh agen, dan penilaian "
       "anti-ban sebelum balasan dikirim.",
    5: "Activity diagram Mengelola Prospek menunjukkan penolakan catatan kosong dan penambahan hitungan konversi saat "
       "prospek dipindah ke tahap daftar.",
    6: "Activity diagram Mengelola Kontak Pelanggan menunjukkan pencarian kontak, kondisi kontak tidak ditemukan, dan "
       "validasi data sebelum disimpan.",
    7: "Activity diagram Melihat Dashboard Pemantauan menunjukkan pengambilan metrik harian, penerapan filter nomor dan "
       "periode, serta kondisi tanpa data.",
    8: "Activity diagram Mengelola Nomor WhatsApp menunjukkan pembuatan kode QR, pembuatan ulang QR yang kedaluwarsa, "
       "dan pencatatan penautan gagal di Pusat Risiko.",
    9: "Activity diagram Mengelola Basis Pengetahuan menunjukkan validasi judul dan isi, lalu pengindeksan ulang FTS5 "
       "setelah artikel disimpan.",
    10: "Activity diagram Mengatur AI dan Anti-ban menunjukkan validasi nilai batas, uji koneksi penyedia AI, dan "
        "enkripsi kunci API sebelum pengaturan disimpan.",
    11: "Activity diagram Mengelola Tim dan Hak Akses menunjukkan penolakan email yang sudah terdaftar dan penyimpanan "
        "akses per nomor.",
    12: "Activity diagram Melihat Log Audit menunjukkan penerapan filter pelaku, aksi, dan tanggal serta kondisi tanpa "
        "hasil.",
}
for i in range(1, 13):
    nama = UC[i - 1][1]
    add("fig", f"ad{i:02d}", f"Activity Diagram {nama} (AD-{i:02d})", PNG + f"AD-{i:02d} - {nama}.png", AD_KET[i])

add("h2", "4.4 Diagram Sequence")
add("p", "Sequence diagram memuat aktor, objek antarmuka (View), pengendali (Cont), dan entitas (Ent) beserta urutan "
         "pesan bernomor sesuai alur normal. Sequence diagram disusun untuk kedua belas use case.")
SD_KET = {
    1: "Cont:Login memeriksa data pengguna, memverifikasi password, mengambil akses nomor, lalu mencatat log audit.",
    2: "WhatsAppGateway berperan sebagai objek antarmuka yang meneruskan pesan pelanggan ke Cont:Percakapan, lalu "
       "Cont:AIEngine menyiapkan balasan.",
    3: "Cont:AIEngine mencari artikel, meminta penyedia AI menyusun jawaban, menghitung keyakinan, lalu meneruskan "
       "jawaban ke Cont:AntiBan sebelum dikirim.",
    4: "Agen mengambil alih percakapan, dan Cont:Percakapan menghentikan AI sebelum balasan agen dinilai mesin anti-ban.",
    5: "Cont:Prospek memuat prospek per tahap, menyimpan perubahan tahap dan aktivitas, lalu menghitung ulang skor.",
    6: "Cont:Kontak mencari kontak berdasarkan kata kunci dan menyimpan perubahan data setelah validasi.",
    7: "Cont:Dashboard mengambil metrik harian dan status nomor, lalu menghitung ulang metrik saat filter diubah.",
    8: "Cont:NomorWA meminta sesi baru, menampilkan kode QR, lalu menyimpan status tersambung setelah QR dipindai.",
    9: "Cont:BasisPengetahuan menyimpan artikel, mengindeks ulang FTS5, dan menjalankan uji pencarian.",
    10: "Cont:PengaturanAI memvalidasi nilai, menguji kunci API ke penyedia AI, lalu menyimpan kunci dalam bentuk "
        "terenkripsi.",
    11: "Cont:TimAkses menyimpan pengguna baru dan matriks akses per nomor, lalu mencatat log audit.",
    12: "Cont:LogAudit mengambil log terbaru dan menampilkan hasil sesuai filter pelaku, aksi, dan tanggal.",
}
for i in range(1, 13):
    nama = UC[i - 1][1]
    add("fig", f"sd{i:02d}", f"Sequence Diagram {nama} (SD-{i:02d})", PNG + f"SD-{i:02d} - {nama}.png", SD_KET[i])

add("h2", "4.5 Diagram Kelas (Class Diagram)")
add("p", "Class diagram disusun dengan tata letak Model-View-Controller (MVC) yang sejalan dengan struktur Laravel. Kolom "
         "kiri berisi kelas antarmuka (UI) beserta atribut dan operasi get dan set, kolom tengah berisi kelas pengendali "
         "(Cont) yang memuat logika setiap use case, dan kolom kanan berisi kelas entitas (Ent) yang mewakili data "
         "tersimpan. Diagram dibagi menjadi dua bagian agar tetap terbaca.")
add("fig", "cd1", "Class Diagram Bagian 1: Layanan Percakapan dan CRM",
    PNG + "Class Diagram SAPA (MVC) Bagian 1 - Layanan Percakapan dan CRM.png",
    "Bagian 1 memuat kelas untuk login, dashboard, kotak masuk, prospek, dan kontak, beserta Cont:AIEngine dan "
    "Cont:AntiBan yang dipanggil saat pesan diproses.")
add("fig", "cd2", "Class Diagram Bagian 2: Pengelolaan Sistem", PNG + "Class Diagram SAPA (MVC) Bagian 2 - "
    "Pengelolaan Sistem.png",
    "Bagian 2 memuat kelas untuk pengelolaan nomor WhatsApp, basis pengetahuan, pengaturan AI, tim dan akses, serta "
    "log audit.")
add("p", "Pada implementasi Laravel, kelas UI menjadi view Blade, kelas Cont menjadi controller atau service class, dan "
         "kelas Ent menjadi model Eloquent yang terhubung ke tabel pada ERD.")

add("h2", "4.6 Entity Relationship Diagram (ERD)")
add("p", "ERD menggambarkan tabel basis data beserta kolom dan relasinya. ERD digambar dengan notasi class pada Visual "
         "Paradigm: setiap tabel diberi stereotype <<table>>, kunci utama ditandai <<PK>>, kunci tamu ditandai <<FK>>, "
         "dan setiap garis relasi berlabel 1 : N. ERD dibagi menjadi dua bagian sesuai kelompok fitur.")
add("fig", "erd1", "ERD Bagian 1: Percakapan dan CRM", PNG + "ERD SAPA Bagian 1 - Percakapan dan CRM.png",
    "Bagian 1 menunjukkan bahwa satu kontak dapat memiliki banyak percakapan dan prospek, satu percakapan memiliki "
    "banyak pesan, dan tabel users menjadi penanggung jawab percakapan, prospek, serta aktivitas prospek.")
add("fig", "erd2", "ERD Bagian 2: Pengelolaan Sistem dan Pengiriman",
    PNG + "ERD SAPA Bagian 2 - Pengelolaan Sistem dan Pengiriman.png",
    "Bagian 2 menunjukkan bahwa nomor_whatsapp menjadi pusat relasi untuk akses pengguna, pengaturan AI, metrik harian, "
    "antrean pesan, dan insiden risiko. Tabel artikel_pengetahuan berdiri sendiri dan diindeks oleh tabel virtual FTS5.")
add("p", "Tabel pengaturan_ai menyatukan pengaturan AI dan anti-ban seperti pada migrasi awal tim. Kolom "
         "nomor_whatsapp_id pada tabel tersebut boleh kosong, yang berarti pengaturan berlaku untuk semua nomor.")

# ====================================================================== BAB V
add("h1", "BAB V", "PERANCANGAN ANTARMUKA (UI/UX)", "5")
add("p", "Bab ini berisi rancangan tampilan SAPA. Rancangan dibuat sebagai mockup high-fidelity di Figma untuk setiap "
         "halaman yang akan dibangun, lalu dipetakan ke kebutuhan fungsional yang dilayaninya.")
add("h2", "5.1 Peta Navigasi (Sitemap) dan Alur Pengguna")
add("p", "Setelah login, pengguna masuk ke halaman awal sesuai role: Dashboard untuk Supervisor dan Administrator, serta "
         "Kotak Masuk untuk Agen/CS. Seluruh halaman diakses dari menu samping yang hanya menampilkan menu sesuai hak "
         "akses pengguna.")
add("fig", "sitemap", "Sitemap SAPA", PNG + "Sitemap SAPA.png",
    "Sitemap pada {fig:sitemap} digambar sebagai class diagram dengan stereotype <<page>>. Setiap halaman mencantumkan "
    "kode kebutuhan fungsional dan role yang dapat membukanya, sedangkan kolom kanan memuat halaman turunan seperti "
    "detail percakapan dan form.")
add("h2", "5.2 Panduan Gaya (Style Guide)")
add("p", "Ketentuan tampilan yang dipakai pada seluruh halaman dirangkum pada {tab:gaya}.")
add("table", "gaya", "Panduan Gaya Antarmuka", ["Elemen", "Ketentuan"], [
    ["Warna utama", "#0F766E (hijau toska) untuk judul sistem, menu aktif, dan tombol utama"],
    ["Warna pendukung", "#F8FAFC (latar halaman), #F0FCFA (menu aktif), #E2E8F0 (garis dan batas kartu), #0F172A "
     "(teks utama)"],
    ["Warna status", "#15803D (tersambung atau berhasil) dan #B45309 pada latar #FFFBEB (peringatan)"],
    ["Jenis huruf", "Inter; judul tebal dan isi reguler"],
    ["Komponen", "Menu samping tetap, kartu putih bertepi tipis dengan sudut membulat, lencana skor dan status berwarna"],
    ["Ikon", "Heroicons versi 2: gaya outline 24 piksel untuk menu samping dan gaya solid 20 piksel untuk tombol dan "
     "lencana; warna mengikuti teks atau warna utama"],
    ["Ukuran rancangan", "Desktop 1440 × 900 piksel; tata letak menyesuaikan layar yang lebih kecil"],
], [3.5, 11.5])
add("h2", "5.3 Rancangan Halaman")
add("p", "Rancangan halaman utama beserta kode kebutuhan fungsional yang dilayani ditampilkan pada subbab berikut. Label "
         "menu pada mockup memakai istilah \"Dasbor\" untuk halaman Dashboard.")
MK = [  # (kunci, judul subbab, kode F, berkas, judul gambar, penjelasan)
    ("mk01", "Halaman Login", "F01", "MK-01-login.png", "Rancangan Halaman Login",
     "Halaman Login berisi form email dan password serta pesan galat ketika kredensial salah. Keterangan di bawah "
     "tombol menjelaskan bahwa akun dibuat Administrator dan login ditahan setelah lima kali gagal."),
    ("mk02", "Halaman Dashboard Pemantauan", "F10", "MK-02-dasbor.png", "Rancangan Halaman Dashboard Pemantauan",
     "Halaman Dashboard menampilkan percakapan masuk, rata-rata waktu balas pertama, percakapan belum dibalas, prospek "
     "baru, grafik percakapan per hari, perbandingan balasan AI dan agen, kinerja per nomor, dan prospek prioritas."),
    ("mk03", "Halaman Kotak Masuk", "F02, F04, F05, F07", "MK-03-kotak-masuk.png", "Rancangan Halaman Kotak Masuk",
     "Halaman Kotak Masuk terdiri atas tiga kolom: daftar percakapan, isi percakapan, dan panel data calon siswa. "
     "Jawaban AI tampil dengan nilai keyakinan dan sumber, dan agen dapat mengambil alih atau menyelesaikan percakapan."),
    ("mk04", "Halaman Prospek", "F08", "MK-04-prospek.png", "Rancangan Halaman Prospek",
     "Halaman Prospek menampilkan papan prospek per tahap dengan skor prioritas berwarna. Detail kartu memuat rincian "
     "skor, riwayat aktivitas, dan form tindak lanjut."),
    ("mk05", "Halaman Kontak", "F03, F09", "MK-05-kontak-daftar.png", "Rancangan Halaman Kontak",
     "Halaman Kontak berisi daftar calon siswa dengan pencarian, filter, dan form ubah data."),
    ("mk06", "Halaman Nomor WhatsApp", "F11", "MK-06-nomor-whatsapp.png", "Rancangan Halaman Nomor WhatsApp",
     "Halaman Nomor WhatsApp menampilkan status sesi, mode AI, dan kesehatan setiap nomor, serta proses penautan "
     "melalui kode QR."),
    ("mk07", "Halaman Basis Pengetahuan", "F12", "MK-07-basis-pengetahuan.png", "Rancangan Halaman Basis Pengetahuan",
     "Halaman Basis Pengetahuan menampilkan artikel per kategori beserta fitur uji pencarian."),
    ("mk08", "Halaman Pengaturan AI dan Konsol Uji", "F13", "MK-08-pengaturan-ai.png",
     "Rancangan Halaman Pengaturan AI dan Konsol Uji",
     "Halaman Pengaturan AI berisi pilihan penyedia AI, ambang keyakinan, kata kunci eskalasi, batas anti-ban, dan "
     "konsol uji keputusan."),
    ("mk09", "Halaman Antrean Keluar dan Pusat Risiko", "F06", "MK-09-antrean-risiko.png",
     "Rancangan Halaman Antrean Keluar dan Pusat Risiko",
     "Halaman ini menampilkan antrean pesan keluar beserta keputusan anti-ban dan daftar insiden pada Pusat Risiko."),
    ("mk10", "Halaman Tim dan Akses", "F14", "MK-10-tim-akses-daftar.png", "Rancangan Halaman Tim dan Akses",
     "Halaman Tim dan Akses berisi daftar pengguna, role, dan matriks akses per nomor WhatsApp."),
    ("mk11", "Halaman Log Audit", "F15", "MK-11-log-audit.png", "Rancangan Halaman Log Audit",
     "Halaman Log Audit menampilkan riwayat tindakan dengan filter pelaku, aksi, dan tanggal, serta detail perubahan."),
]
for k, (key, sub, kode, fn, judul, desk) in enumerate(MK, 1):
    add("h3", f"5.3.{k} {sub} ({kode})")
    add("fig", key, judul, MOCK + fn, desk)

# ====================================================================== BAB VI
add("h1", "BAB VI", "METODE PENGEMBANGAN SISTEM", "6")
add("h2", "6.1 System Development Life Cycle")
add("p", "Pengembangan SAPA menggunakan Scrum, kerangka kerja Agile yang membangun produk secara bertahap melalui sprint "
         "dengan durasi tetap (Schwaber & Sutherland, 2020). Scrum dipilih karena mitra dapat memberi masukan pada "
         "setiap Sprint Review dan perubahan kebutuhan dapat dimasukkan ke Product Backlog tanpa mengubah seluruh "
         "rencana. Siklus Scrum pada proyek ini ditunjukkan pada {fig:scrum}.")
add("fig", "scrum", "Activity Diagram Siklus Scrum Proyek SAPA", PNG + "AD-Scrum - Siklus Scrum Proyek SAPA.png",
    "Product Owner menyusun Product Backlog, tim memilih PBI pada Sprint Planning, lalu mengerjakan dan menguji PBI "
    "dengan Daily Scrum setiap hari. Di akhir sprint, Increment didemokan pada Sprint Review, tim melakukan Sprint "
    "Retrospective, dan siklus berulang sampai Sprint 3 selesai.")
add("p", "Proyek berjalan dalam tiga sprint, masing-masing dua minggu, dimulai Senin, 9 November 2026. Sebelum Sprint 1 "
         "terdapat pra-sprint untuk inisiasi proyek, requirement gathering, laporan ASN1, UML, dan mockup Figma. "
         "Pembagian role Scrum adalah sebagai berikut.")
add("ol", [
    "**Product Owner dan Scrum Master: Yordan.** Kedua role digabung karena tim hanya lima orang. Yordan mengurutkan "
    "Product Backlog, memimpin acara Scrum, dan menyampaikan progres kepada mitra.",
    "**Tim pengembang.** Rifqi (backend developer), Isnaini (frontend developer), Enrico (UI/UX designer), dan Agung "
    "(QA/tester dan dokumentasi).",
    "**Stakeholder: Greta.** Pemilik Bimbingan Belajar Asentra yang memberi masukan pada Sprint Review dan menerima demo "
    "akhir.",
])
add("p", "Sprint Planning (2 jam) diadakan pada 9 November, 23 November, dan 7 Desember 2026. Daily Scrum berlangsung "
         "15 menit setiap hari kerja. Sprint Review (1 jam) dan Sprint Retrospective (45 menit) diadakan pada 20 "
         "November, 4 Desember, dan 18 Desember 2026; Sprint Review terakhir sekaligus menjadi demo akhir bersama "
         "mitra. Progres harian dicatat pada papan Trello dan riwayat commit GitHub.")
add("p", "Kapasitas tim dihitung dari lima anggota, sepuluh hari kerja per sprint, 4 jam produktif per hari, dan "
         "kalibrasi 6 jam per Story Point, yaitu 200 jam atau 33 Story Point per sprint. Sebuah Increment dianggap "
         "selesai (Definition of Done) apabila memenuhi syarat sebagai berikut.")
add("ol", [
    "Kode digabung ke cabang utama melalui pull request setelah ditinjau anggota lain.",
    "Uji fitur lulus untuk alur normal, hak akses per nomor, dan kondisi galat sesuai rincian kebutuhan.",
    "Fitur berjalan pada lingkungan uji (VPS) dengan nomor WhatsApp uji tanpa menyentuh data mitra.",
    "Antarmuka sesuai mockup Figma dan dapat didemokan kepada Product Owner pada Sprint Review.",
    "Dokumentasi diperbarui dan perubahan tercatat pada log audit apabila relevan.",
])
add("h2", "6.2 User Story")
add("p", "Kebutuhan fungsional diturunkan menjadi user story dengan kriteria penerimaan dan estimasi Story Point seperti "
         "pada {tab:us}.")
add("table", "us", "Daftar User Story", ["Kode", "User story", "Kriteria penerimaan", "Kode F", "SP"], [
    ["US01", "Sebagai pengguna, saya ingin login dengan email dan password agar hanya akun berhak yang memakai SAPA "
     "sesuai role dan nomor WhatsApp-nya.", "Login berhasil dengan akun aktif; ditolak apabila data salah atau akun "
     "nonaktif; ditahan 5 menit setelah lima kali gagal.", "F01", "5"],
    ["US02", "Sebagai administrator, saya ingin menautkan nomor WhatsApp dengan memindai kode QR agar semua nomor mitra "
     "terpusat.", "Nomor tersambung setelah QR dipindai; QR kedaluwarsa dapat dibuat ulang.", "F11", "8"],
    ["US03", "Sebagai agen, saya ingin melihat dan membalas percakapan dari semua nomor di satu kotak masuk agar tidak "
     "berpindah ponsel.", "Percakapan dari nomor yang diizinkan tampil dan dapat dibalas; nomor lain ditolak.",
     "F02, F07", "8"],
    ["US04", "Sebagai tim pengembang, kami ingin repositori, struktur proyek Laravel, dan skema basis data siap agar "
     "pengembangan fitur dapat berjalan.", "Repositori, struktur proyek, migrasi tabel awal, dan WA Gateway dasar siap "
     "dipakai (enabler).", "-", "3"],
    ["US05", "Sebagai supervisor, saya ingin mengelola artikel basis pengetahuan dengan pencarian teks penuh agar AI "
     "menjawab sesuai sumber resmi.", "Artikel dapat ditambah, diubah, dan dinonaktifkan; terindeks ulang FTS5; ada uji "
     "pencarian.", "F12", "5"],
    ["US06", "Sebagai calon siswa atau orang tua, saya ingin pertanyaan saya dijawab otomatis dengan sumber yang jelas "
     "agar tidak menunggu admin.", "Jawaban AI menyertakan sumber; tanpa artikel relevan, percakapan dialihkan ke agen.",
     "F04", "8"],
    ["US07", "Sebagai agen, saya ingin data calon siswa (jenjang, kelas, mapel) terisi otomatis dari chat agar tidak "
     "perlu input manual.", "Jenjang, kelas, dan mapel terisi dari chat dan skor prioritas diperbarui.", "F03", "5"],
    ["US08", "Sebagai administrator, saya ingin mengatur penyedia AI, ambang keyakinan, dan kata kunci eskalasi agar "
     "perilaku AI terkendali.", "Pengaturan tersimpan dan berlaku; kunci API terenkripsi; konsol uji menampilkan jejak "
     "keputusan.", "F13", "3"],
    ["US09", "Sebagai agen, saya ingin AI berhenti membalas dan menyerahkan percakapan saat tidak yakin agar pertanyaan "
     "sulit ditangani manusia.", "AI berhenti membalas saat keyakinan rendah, ada kata kunci eskalasi, atau nada marah.",
     "F05", "5"],
    ["US10", "Sebagai agen, saya ingin mengelola prospek per tahap dengan skor prioritas yang dapat dijelaskan agar tahu "
     "siapa yang didahulukan.", "Prospek tampil per tahap dengan skor dan rinciannya; tahap dapat dipindah; catatan "
     "wajib diisi.", "F08", "5"],
    ["US11", "Sebagai agen, saya ingin mengelola data kontak calon siswa agar riwayat tersimpan rapi.",
     "Kontak dapat dicari dan diubah; nomor tidak valid atau duplikat ditolak.", "F09", "2"],
    ["US12", "Sebagai administrator, saya ingin pengiriman pesan dibatasi dan dijeda agar nomor mitra tidak diblokir.",
     "Pesan dinilai kirim, tunda, atau tahan; pesan melebihi batas tertunda di antrean; insiden tercatat.", "F06", "8"],
    ["US13", "Sebagai supervisor, saya ingin dashboard per nomor agar kinerja layanan terpantau.",
     "Dashboard menampilkan empat metrik per nomor dengan filter nomor dan periode.", "F10", "5"],
    ["US14", "Sebagai supervisor, saya ingin log audit dan pusat risiko agar setiap perubahan dan insiden dapat "
     "ditelusuri.", "Log audit dapat difilter berdasarkan pelaku, aksi, dan tanggal; insiden tampil di Pusat Risiko.",
     "F15", "5"],
    ["US15", "Sebagai administrator, saya ingin mengelola pengguna, role, dan hak akses per nomor agar akses sesuai "
     "tugas.", "Pengguna dan akses nomor tersimpan dan langsung berlaku; email duplikat ditolak.", "F14", "3"],
    ["US16", "Sebagai tim, kami ingin pengujian menyeluruh dan perbaikan bug agar sistem siap dipakai mitra.",
     "Uji fungsi, hak akses, dan penautan QR lulus; UAT dengan kuesioner SUS dilakukan; laporan pengujian tersedia.",
     "Semua", "8"],
    ["US17", "Sebagai tim, kami ingin laporan akhir, diagram UML, dan panduan pengguna final agar proyek terdokumentasi.",
     "Laporan akhir, berkas Visual Paradigm, dan panduan pengguna final tersedia.", "-", "3"],
], [1.2, 5.6, 5.4, 1.6, 1.2])
add("p", "Total estimasi seluruh user story adalah 89 Story Point. Estimasi dinilai ulang oleh tim pengembang saat Sprint "
         "Planning dengan Planning Poker.")
add("h2", "6.3 Rencana Iterasi / Sprint")
add("p", "User story dibagi ke dalam tiga sprint dengan komitmen yang tidak melebihi kapasitas 33 Story Point, seperti "
         "pada {tab:sprint}.")
add("table", "sprint", "Rencana Iterasi Pengembangan", ["Iterasi", "Periode", "User story", "Target keluaran"], [
    ["Pra-sprint", "Sebelum 9 November 2026", "-", "Inisiasi proyek, requirement gathering, laporan ASN1, UML, mockup "
     "Figma, dan SRS"],
    ["Sprint 1", "Week 1–2 (9–22 November 2026)", "US01–US04 (24 SP)", "Fondasi sistem: login dan RBAC, penautan nomor "
     "WhatsApp melalui QR, kotak masuk, repositori Laravel, skema basis data, dan WA Gateway dasar"],
    ["Sprint 2", "Week 3–4 (23 November–6 Desember 2026)", "US05–US11 (33 SP)", "Fitur inti: jawaban AI dengan FTS5, "
     "klasifikasi maksud, eskalasi ke agen, CRM prospek, dan kontak"],
    ["Sprint 3", "Week 5–6 (7–20 Desember 2026)", "US12–US17 (32 SP)", "Penguatan dan rilis: anti-ban, dashboard, log "
     "audit, tim dan akses, pengujian akhir, dokumentasi, dan demo akhir kepada mitra"],
], [2.2, 4.0, 3.0, 5.8])
add("p", "Per 17 November 2026, Sprint 1 sedang berjalan. Repositori Laravel tim telah berisi migrasi awal untuk tabel "
         "pengguna, nomor WhatsApp, akses nomor, pesan, pengaturan AI, antrean pesan, insiden risiko, dan prospek, "
         "serta kerangka halaman untuk menu utama.")

# ====================================================================== DAFTAR PUSTAKA (APA 7)
PUSTAKA = [
    "Fan, W., Ding, Y., Ning, L., Wang, S., Li, H., Yin, D., Chua, T.-S., & Li, Q. (2024). A survey on RAG meeting "
    "LLMs: Towards retrieval-augmented large language models. In *Proceedings of the 30th ACM SIGKDD Conference on "
    "Knowledge Discovery and Data Mining* (pp. 6491–6501). ACM. https://doi.org/10.1145/3637528.3671470",
    "González-Flores, L., Rubiano-Moreno, J., & Sosa-Gómez, G. (2025). The relevance of lead prioritization: A B2B lead "
    "scoring model based on machine learning. *Frontiers in Artificial Intelligence, 8*, 1554325. "
    "https://doi.org/10.3389/frai.2025.1554325",
    "IEEE. (1998). *IEEE recommended practice for software requirements specifications* (IEEE Std 830-1998). IEEE. "
    "https://doi.org/10.1109/IEEESTD.1998.88286",
    "Imaduddin, M., Susanto, R., & Pradana, A. I. (2026). Pengembangan chatbot WhatsApp berbasis retrieval-augmented "
    "generation (RAG) dan OpenAI untuk penyediaan jawaban akurat dari dokumen aturan organisasi. *Adopsi Teknologi dan "
    "Sistem Informasi (ATASI), 5*(1), 23–31. https://doi.org/10.30872/atasi.v5i1.3472",
    "ISO/IEC/IEEE. (2018). *Systems and software engineering: Life cycle processes: Requirements engineering* "
    "(ISO/IEC/IEEE 29148:2018). https://doi.org/10.1109/IEEESTD.2018.8559686",
    "Narulita, S., Nugroho, A., & Abdillah, M. Z. (2024). Diagram unified modelling language (UML) untuk perancangan "
    "sistem informasi manajemen penelitian dan pengabdian masyarakat (SIMLITABMAS). *Bridge: Jurnal Publikasi Sistem "
    "Informasi dan Telekomunikasi, 2*(3), 244–256. https://doi.org/10.62951/bridge.v2i3.174",
    "Republik Indonesia. (2022). *Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data "
    "Pribadi*. Sekretariat Negara. https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022",
    "Schwaber, K., & Sutherland, J. (2020). *The Scrum guide: The definitive guide to Scrum: The rules of the game*. "
    "https://scrumguides.org/scrum-guide.html",
    "Wolf, L., & Steul-Fischer, M. (2023). Factors of customers' channel choice in an omnichannel environment: A "
    "systematic literature review. *Management Review Quarterly, 73*(4), 1579–1630. "
    "https://doi.org/10.1007/s11301-022-00281-w",
]

# ====================================================================== LAMPIRAN
LAMPIRAN = []


def lamp(*blk):
    LAMPIRAN.append(blk)


lamp("h2app", "Lampiran A. Matriks Keterlacakan Kebutuhan (Traceability Matrix)", "A")
lamp("p", "Matriks pada {tab:trace} memastikan setiap kebutuhan fungsional dapat ditelusuri dari use case, user story, "
          "dan rancangan halaman sampai kode uji. Status diperbarui setiap Sprint Review.")
TRACE = [  # F, UC, US, gambar, sprint
    ("F01", "UC-01", "US01", "mk01", "Sprint 1, berjalan"), ("F02", "UC-02", "US03", "mk03", "Sprint 1, berjalan"),
    ("F03", "UC-02, UC-03", "US07", "mk05", "Sprint 2"), ("F04", "UC-03", "US06", "mk03", "Sprint 2"),
    ("F05", "UC-03, UC-04", "US09", "mk03", "Sprint 2"), ("F06", "UC-03, UC-04, UC-10", "US12", "mk09", "Sprint 3"),
    ("F07", "UC-04", "US03", "mk03", "Sprint 1, berjalan"), ("F08", "UC-05", "US10", "mk04", "Sprint 2"),
    ("F09", "UC-06", "US11", "mk05", "Sprint 2"), ("F10", "UC-07", "US13", "mk02", "Sprint 3"),
    ("F11", "UC-08", "US02", "mk06", "Sprint 1, berjalan"), ("F12", "UC-09", "US05", "mk07", "Sprint 2"),
    ("F13", "UC-10", "US08", "mk08", "Sprint 2"), ("F14", "UC-11", "US15", "mk10", "Sprint 3"),
    ("F15", "UC-12", "US14", "mk11", "Sprint 3"),
]
lamp("table", "trace", "Matriks Keterlacakan Kebutuhan", ["Kode F", "Use case", "User story", "Halaman UI",
                                                          "Kode uji", "Status"],
     [[f, uc, us, "{fig:" + mk + "}", "TC" + f[1:], st] for f, uc, us, mk, st in TRACE], [1.6, 3.4, 2.0, 2.6, 1.8, 3.6])

lamp("h2app", "Lampiran B. Hasil Requirement Gathering", "B")
lamp("p", "Profil mitra dan ringkasan hasil requirement gathering bersama pemilik Bimbingan Belajar Asentra dirangkum "
          "pada {tab:mitra}.")
lamp("table", "mitra", "Profil Mitra dan Hasil Requirement Gathering", ["Aspek", "Keterangan"], [
    ["Nama mitra", "Bimbingan Belajar Asentra"],
    ["Bidang usaha", "Jasa pendidikan nonformal (bimbingan belajar)"],
    ["Layanan", "Kelas eksklusif, program reguler, dan kelas persiapan tes kemampuan akademik"],
    ["Alamat", "Grasak, Gondang, Kec. Gondang, Kabupaten Sragen, Jawa Tengah 57254"],
    ["Tahun berdiri", "2024"],
    ["Jumlah siswa aktif", "128 siswa"],
    ["Pengajar dan staf", "24 pengajar, 1 admin, 2 sales"],
    ["Jenjang", "Pra-sekolah, SD, SMP, dan SMA"],
    ["Kanal layanan saat ini", "Lebih dari satu nomor WhatsApp, yaitu nomor admin dan nomor sales"],
    ["Narasumber", "Greta (Owner)"],
    ["Tanggal wawancara", "Sabtu, 26 September 2026; data profil dikonfirmasi tertulis pada 9 Oktober 2026"],
    ["Kondisi sebelum sistem", "Pertanyaan dijawab manual dari ponsel masing-masing; percakapan terpisah per perangkat; "
     "data calon siswa tidak tercatat; tidak ada pemantauan per nomor"],
    ["Kebutuhan utama", "Kotak masuk terpadu, jawaban otomatis dari katalog resmi, pencatatan calon siswa, hak akses per "
     "nomor, dan pemantauan kinerja"],
    ["Data yang diolah", "Katalog program, basis pengetahuan (FAQ), percakapan WhatsApp, data calon siswa, pengguna dan "
     "nomor WhatsApp, metrik harian per nomor, dan log audit"],
], [4.0, 11.0])
lamp("p", "Requirement gathering dilakukan melalui wawancara daring dengan pemilik Asentra. Informasi rapat dicatat pada "
          "{tab:momrapat}, dan hasil pembahasan beserta tindak lanjutnya dicatat dalam format notulen rapat (minutes of "
          "meeting) pada {tab:mom}.")
lamp("table", "momrapat", "Informasi Rapat Requirement Gathering", ["Aspek", "Keterangan"], [
    ["Kegiatan", "Wawancara requirement gathering sistem SAPA"],
    ["Hari, tanggal", "Sabtu, 26 September 2026"],
    ["Waktu", "10.00–11.30 WIB"],
    ["Tempat", "Daring melalui Google Meet"],
    ["Narasumber", "Greta (Owner, Bimbingan Belajar Asentra)"],
    ["Peserta", "Kelompok 1: Yordan (Product Owner, pengusul proyek), Rifqi, Isnaini, Agung, dan Enrico"],
    ["Notulis", "Agung"],
    ["Agenda", "1. Profil dan layanan Asentra\n2. Alur layanan calon siswa melalui WhatsApp\n3. Masalah yang dihadapi "
     "admin dan sales\n4. Kebutuhan sistem dan batasan rilis\n5. Keterlibatan mitra selama pengembangan"],
], [3.5, 11.5])
lamp("table", "mom", "Notulen Hasil Pembahasan Requirement Gathering", ["No", "Topik", "Hasil pembahasan",
                                                                         "Tindak lanjut", "PIC"], [
    ["1", "Profil Asentra", "Asentra berdiri pada 2024 dan melayani 128 siswa dari jenjang pra-sekolah sampai SMA dengan "
     "24 pengajar, satu admin, dan dua sales.", "Data profil dikirim tertulis kepada tim (selesai 9 Oktober 2026).",
     "Yordan"],
    ["2", "Alur pertanyaan calon siswa", "Calon siswa menghubungi nomor admin atau nomor sales. Pertanyaan terbanyak "
     "adalah jadwal, biaya, fasilitas, dan cara pendaftaran, dan semuanya dijawab manual dari ponsel.",
     "Pertanyaan berulang dijawab otomatis dari basis pengetahuan (F04, F05).", "Rifqi"],
    ["3", "Informasi program", "Informasi program beredar sebagai kartu gambar dan belum tersedia dalam bentuk teks.",
     "Mitra menyiapkan katalog program dan FAQ dalam bentuk teks untuk basis pengetahuan (F12).", "Yordan"],
    ["4", "Pencatatan calon siswa", "Data calon siswa tidak dicatat, dan tindak lanjut bergantung pada ingatan sales.",
     "Kontak dan prospek dibuat otomatis, lengkap dengan tahap dan skor prioritas (F03, F08, F09).",
     "Rifqi, Isnaini"],
    ["5", "Pembagian nomor dan hak akses", "Nomor admin dan nomor sales dipegang orang berbeda. Pemilik ingin melihat "
     "semua percakapan, sedangkan staf cukup melihat nomor yang dipegangnya.",
     "Login dengan role dan akses per nomor (F01, F14).", "Rifqi"],
    ["6", "Pemantauan layanan", "Pemilik ingin mengetahui jumlah chat masuk, chat yang belum dibalas, kecepatan balasan, "
     "dan jumlah calon siswa yang mendaftar per nomor.", "Dashboard per nomor (F10).", "Isnaini, Enrico"],
    ["7", "Risiko nomor dan data pribadi", "Pemilik khawatir nomor diblokir apabila bot membalas terlalu cepat, dan data "
     "calon siswa tidak boleh tersebar.", "Mesin anti-ban tanpa broadcast, akses terbatas, dan log audit (F06, F15, "
     "NF09, NF11).", "Rifqi, Agung"],
    ["8", "Batasan rilis", "Pembayaran, data akademik, pesan broadcast, dan kanal selain WhatsApp belum dibutuhkan.",
     "Dicatat sebagai di luar cakupan dan Won't have ({tab:lingkup}, {tab:fr}).", "Yordan"],
    ["9", "Keterlibatan mitra", "Pemilik bersedia memberi masukan pada setiap Sprint Review. Pengujian memakai nomor "
     "WhatsApp cadangan, bukan nomor operasional.", "Jadwal Sprint Review dimasukkan ke perencanaan sprint.", "Yordan"],
], [0.9, 2.9, 5.0, 4.4, 1.8])

lamp("h2app", "Lampiran C. Daftar Hal yang Belum Ditentukan (TBD)", "C")
lamp("p", "Hal yang belum ditentukan pada saat dokumen ini disusun dicatat pada {tab:tbd} beserta penanggung jawab dan "
          "target waktunya.")
lamp("table", "tbd", "Daftar Hal yang Belum Ditentukan", ["No", "Hal yang belum ditentukan", "Penanggung jawab",
                                                          "Target waktu"], [
    ["1", "NIDN dosen pengampu pada lembar pengesahan", "Ketua kelompok (Yordan)", "Sebelum pengumpulan SRS"],
    ["2", "Konfirmasi isi notulen requirement gathering ({tab:mom}) kepada mitra", "Product Owner (Yordan)",
     "20 November 2026"],
    ["3", "Konfirmasi daftar di luar cakupan ({tab:lingkup}) dan tingkat keahlian pengguna ({tab:pengguna}) dengan mitra",
     "Product Owner (Yordan)", "20 November 2026 (Sprint Review 1)"],
    ["4", "Penyelarasan migrasi tim dengan ERD: tabel kontak dan percakapan belum ada, dan tabel prospek masih "
     "menyimpan nama serta nomor telepon secara langsung", "Backend (Rifqi) dan frontend (Isnaini)",
     "22 November 2026 (akhir Sprint 1)"],
    ["5", "Label menu \"Dasbor\" atau \"Dashboard\" pada antarmuka", "UI/UX (Enrico)",
     "22 November 2026"],
    ["6", "Penyedia AI yang dipakai mitra dan anggaran biaya pemanggilan API", "Product Owner (Yordan)",
     "23 November 2026 (awal Sprint 2)"],
    ["7", "Komponen, bobot, dan ambang lima komponen skor prioritas prospek", "Backend (Rifqi)", "30 November 2026"],
    ["8", "Nilai batas anti-ban (per menit, per jam, per hari, jeda, jam aktif)", "Backend (Rifqi)", "7 Desember 2026"],
    ["9", "Cara menjalankan WA Gateway di VPS (process manager) dan versi Baileys yang dikunci", "Backend (Rifqi)",
     "22 November 2026"],
    ["10", "Jumlah pengguna bersamaan, target ketersediaan (NF08), dan target SUS (NF10)", "Product Owner (Yordan)",
     "7 Desember 2026 (awal Sprint 3)"],
], [1.0, 7.4, 3.6, 3.0])


# ====================================================================== kamus data (keterangan kolom)
KAMUS_TABEL = ["users", "user_whatsapp_access", "nomor_whatsapp", "pengaturan_ai", "kontak", "percakapan",
               "pesan_whatsapp", "prospek", "aktivitas_prospek", "artikel_pengetahuan", "antrean_pesan",
               "riwayat_antrean", "insiden_risiko", "metrik_harian", "log_audit"]
KET = {
    "id": "Kunci utama", "name": "Nama pengguna", "email": "Email login, unik", "password": "Hash bcrypt",
    "role": "Agen/CS, Supervisor, atau Administrator", "user_id": "FK ke users",
    "nomor_whatsapp_id": "FK ke nomor_whatsapp", "hak_akses": "Level akses pengguna pada nomor (baca atau balas)",
    "label": "Nama tampilan atau label", "nomor": "Nomor WhatsApp, unik", "tujuan": "Admin atau sales",
    "status": "Status data (lihat aturan bisnis)", "mode_ai": "Otomatis, draf, atau mati",
    "skor_kesehatan": "Skor kesehatan nomor 0–100", "penyedia": "Penyedia AI", "model": "Nama model AI",
    "api_key": "Kunci API terenkripsi", "instruksi_persona": "Gaya bahasa AI",
    "ambang_keyakinan": "Batas keyakinan untuk eskalasi (0–1)", "kata_kunci_eskalasi": "Daftar kata pemicu eskalasi",
    "jeda_min": "Jeda minimum antarpesan (detik)", "jeda_max": "Jeda maksimum antarpesan (detik)",
    "batas_per_menit": "Batas pesan keluar per menit", "batas_per_jam": "Batas pesan keluar per jam",
    "batas_pesan_harian": "Batas pesan keluar per hari", "jam_mulai": "Awal jam aktif pengiriman",
    "jam_selesai": "Akhir jam aktif pengiriman", "nomor_telepon": "Nomor WhatsApp pelanggan, unik",
    "nama": "Nama calon siswa atau orang tua", "jenjang": "Pra-sekolah, SD, SMP, atau SMA", "kelas": "Kelas",
    "mapel": "Mata pelajaran yang diminati", "kota": "Kota asal", "sumber": "Sumber kontak",
    "kontak_id": "FK ke kontak", "agen_id": "FK ke users, agen penangan", "penangan": "AI atau agen",
    "belum_dibaca": "Jumlah pesan belum dibaca", "waktu_balas_pertama": "Waktu balas pertama (detik)",
    "percakapan_id": "FK ke percakapan", "arah": "Masuk atau keluar", "jenis_pengirim": "Pelanggan, AI, atau agen",
    "isi": "Isi teks", "meta_ai": "Jejak keputusan AI (JSON)", "penanggung_jawab": "FK ke users, pemilik prospek",
    "tahap": "Baru, dihubungi, tertarik, penawaran, daftar, atau batal", "skor": "Skor prioritas 0–100",
    "rincian_skor": "Rincian lima komponen skor (JSON)", "program": "Program yang diminati",
    "tindak_lanjut_berikut": "Tanggal tindak lanjut berikutnya", "prospek_id": "FK ke prospek",
    "jenis": "Jenis aktivitas", "catatan": "Catatan aktivitas, wajib", "waktu": "Waktu aktivitas",
    "judul": "Judul artikel", "kategori": "Program, jadwal, biaya, fasilitas, atau pendaftaran",
    "aktif": "Artikel dipakai AI atau tidak", "pesan_whatsapp_id": "FK ke pesan_whatsapp, boleh kosong",
    "penerima": "Nomor tujuan", "isi_pesan": "Isi pesan keluar", "skor_risiko": "Skor risiko anti-ban 0–100",
    "keputusan": "Kirim, tunda, atau tahan", "percobaan": "Jumlah percobaan kirim",
    "jadwal_kirim": "Waktu kirim terjadwal", "terkirim_pada": "Waktu terkirim",
    "alasan_penahanan": "Alasan pesan ditunda atau ditahan", "antrean_pesan_id": "FK ke antrean_pesan",
    "status_sebelumnya": "Status antrean sebelum berubah", "status_baru": "Status antrean setelah berubah",
    "keterangan": "Keterangan perubahan", "diubah_pada": "Waktu perubahan", "jenis_insiden": "Jenis insiden risiko",
    "tingkat_risiko": "Rendah, sedang, atau tinggi", "deskripsi": "Uraian insiden", "terjadi_pada": "Waktu kejadian",
    "tanggal": "Tanggal metrik", "pesan_masuk": "Jumlah pesan masuk", "pesan_keluar": "Jumlah pesan keluar",
    "balasan_ai": "Jumlah balasan AI", "balasan_manusia": "Jumlah balasan agen",
    "belum_dibalas": "Jumlah percakapan belum dibalas", "rata_waktu_balas": "Rata-rata waktu balas pertama (detik)",
    "prospek_baru": "Jumlah prospek baru", "konversi": "Jumlah prospek tahap daftar",
    "aksi": "Jenis aksi", "entitas": "Nama tabel yang terdampak", "entitas_id": "id baris yang terdampak",
    "detail": "Detail perubahan (JSON)", "created_at": "Waktu kejadian",
}
