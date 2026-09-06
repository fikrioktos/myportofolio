# Portfolio PBP — Fikri Okto Setiadi

Website portofolio pribadi untuk mata kuliah **Pemrograman Berbasis Platform (PBP)**, Fakultas Ilmu Komputer Universitas Indonesia, Semester Gasal 2026/2027.

## Identitas

- **Nama:** Fikri Okto Setiadi
- **NPM:** 2506621655
- **Kelas:** PBP D
- **Angkatan:** 2025

## Tentang Proyek

Repository ini berisi website portofolio pribadi yang dibangun menggunakan **Django** sebagai framework backend dan **HTML5 + CSS3 murni** untuk frontend. Proyek ini adalah kelanjutan dari Tutorial 01 dan akan berkembang setiap minggunya seiring tugas individu PBP.

**Live demo:** [https://fikri-okto-myportofolio.pws.cs.ui.ac.id](https://fikri-okto-myportofolio.pws.cs.ui.ac.id)

## Tech Stack

| Layer | Teknologi |
|---|---|
| Backend | Django 6.1 |
| Frontend | HTML5 + CSS3 murni (no framework, no JavaScript) |
| Web server (production) | Gunicorn |
| Static files | WhiteNoise middleware |
| Database (local) | SQLite |
| Database (production) | PostgreSQL via PWS |
| Environment management | python-dotenv |
| Deployment | PWS (Pacil Web Service) Fasilkom UI |
| Version control | Git + GitHub |

## Branching & Workflow

Project ini menggunakan **trunk-based development** dengan feature branches:

- Branch utama: `master` (sync dengan `origin/main` dan `pws/master`)
- Feature branch naming: `<type>/<deskripsi>` (mis. `feat/skills-section`, `fix/profile`, `style/responsive`)
- Conventional Commits untuk pesan commit (type + scope + deskripsi bahasa Indonesia)
- Dua remote:
  - `origin` — GitHub (untuk submit & review)
  - `pws` — PWS Fasilkom (untuk deployment)

## Struktur Proyek

```
myportofolio/
├── manage.py                # entry point Django
├── requirements.txt         # dependency list (Django, gunicorn, whitenoise, dll.)
├── .env / .env.prod         # environment variables (tidak di-track git)
├── portofolio/              # package konfigurasi Django (settings, urls, views)
├── templates/
│   └── index.html           # template utama halaman portofolio
├── static/
│   ├── css/style.css        # styling seluruh halaman
│   └── img/okto.png         # foto profil
└── staticfiles/             # output `collectstatic` untuk production (tidak di-track)
```

## Setup Lokal

1. **Aktifkan virtual environment:**
   ```bash
   source env/Scripts/activate      # Windows (bash)
   # atau: env\Scripts\activate.bat # Windows (cmd)
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Pastikan `.env` ada** dengan isi minimal:
   ```
   PRODUCTION=False
   ```

4. **Jalankan server:**
   ```bash
   python manage.py runserver
   ```
   Buka `http://localhost:8000/` di browser.

## Deployment

Project ini di-deploy ke **PWS (Pacil Web Service)** Fasilkom UI. URL deployment: `https://fikri-okto-myportofolio.pws.cs.ui.ac.id`. Untuk re-deploy:

```bash
git push pws master
```

## Progres Mingguan

### ✅ Tutorial 01 — Setup Django, HTML5 & CSS3 (31 Agustus 2026)
- Setup project Django dengan folder `myportofolio/` (root) dan `portofolio/` (config).
- Halaman About Me dengan hero section: foto, nama, NPM, bio, social links.
- Semantic HTML5 (`<header>`, `<main>`, `<section>`, `<footer>`).
- Styling dengan CSS custom properties (palette cream + terracotta), Flexbox untuk header, Grid untuk hero layout.
- Responsive media query untuk mobile (≤600px).
- Deployment ke PWS Fasilkom UI.

### ✅ Tugas 1 — Section Baru & Interaktivitas (4 September 2026)
- **Skills section** — grid 3 kolom dengan 8 skill items (Programming, ML/Data, Languages).
- **Experience section** — timeline layout dengan 4 entry (RISTEK, TA DDP 1, BEM UI, DDP 0).
- **Multi-link navigation** — header dengan 3 link (Profile, Skills, Experience).
- **Sticky header** — header tetap nempel di atas saat scroll.
- **Smooth scroll** — `scroll-behavior: smooth` + `scroll-margin-top` untuk kompensasi header.
- Konfigurasi WhiteNoise untuk static files di production.
- Branching terorganisir: 3 feature branch (`feat/skills-section`, `feat/experience-section`, `style/interactive-navigation`) di-merge ke `master` dengan `--no-ff`.

### Known Issues & Tech Debt

- `SECRET_KEY` masih di-hardcode di `settings.py` (default `django-admin startproject`). Idealnya pindah ke `os.getenv('SECRET_KEY')` agar tidak terekspos di repository public. **Mitigasi sementara:** repository ini masih development, belum ada user/session yang perlu diamankan.
- `DEBUG = True` di-hardcode. Untuk production yang aman, harus dibungkus dengan logika `if PRODUCTION: DEBUG = False`.
- Responsive breakpoint hanya 600px. Tablet (600-900px) belum dites secara eksplisit — perlu ditambahkan media query intermediate di iterasi berikutnya.
- Tidak ada automated tests. Untuk project serius, perlu ditambahkan pytest + Django TestCase minimal untuk view utama.

### Tugas-tugas berikutnya akan ditambahkan di sini seiring semester berlangsung.

---

## AI Disclosure

Project ini dikembangkan dengan bantuan AI assistant (Hermes, model MiniMax-M3). AI digunakan secara terbatas untuk **panduan workflow, code review, dan snippet CSS/HTML**, sementara eksekusi edit, commit, dan push dilakukan sendiri oleh saya.

### Tools yang digunakan
- **Hermes** (desktop chat assistant) untuk diskusi teknis, tanya-jawab soal Git, Django, dan CSS

### Strategi prompting
Saya menggunakan AI sebagai **pair-programming partner**: AI memberikan draft kode/strategi, lalu saya review, modifikasi, dan eksekusi sendiri. Pendekatan ini dipilih agar saya tetap memahami setiap perubahan yang masuk ke repository, bukan hanya copy-paste tanpa paham.

### Bagian yang dibantu AI
- Struktur awal HTML untuk section baru (Skills, Experience)
- CSS pattern: grid layout, timeline layout, sticky header, smooth scroll
- Panduan branching Git (konsep, workflow, conflict resolution)
- Review perubahan sebelum commit (cek duplikat, typo, konvensi pesan commit)
- Template pesan commit Conventional Commits dalam bahasa Indonesia

### Bagian yang saya kerjakan sendiri
- Identitas di website (nama, NPM, bio, social links)
- Konten section berdasarkan data pribadi (skills, pengalaman dari CV)
- Penulisan pesan commit akhir
- Eksekusi semua perintah git (add, commit, push, merge, conflict resolution)
- Review dan koreksi manual terhadap output AI (misalnya koreksi format judul experience, penyesuaian pesan commit)
- Pengujian lokal (`python manage.py runserver`) dan verifikasi visual

### Analisis Kritis Keterbatasan AI

Selama pengerjaan Tugas 1, saya menemukan dua keterbatasan utama AI yang perlu dicatat:

1. **Kurangnya pemahaman konteks dunia nyata.** Dalam satu kesempatan, AI secara keliru menyusun judul section experience untuk peran Teaching Assistant saya. AI menulis `"DDP 1 Fasilkom UI"` sebagai judul, padahal yang lebih tepat adalah `"Teaching Assistant"` (judul peran) dengan `"Dasar-Dasar Pemrograman 1 · Fasilkom UI"` sebagai subjudul konteks. AI cenderung menyusun struktur berdasarkan pola yang sering dilihat di template, bukan memahami relasi semantik antara peran dan nama mata kuliah. Saya perlu mengoreksi ini secara manual karena AI tidak otomatis tahu konvensi penulisan yang lebih baik untuk konteks spesifik saya.

2. **Konsistensi workflow tidak dijamin 100%.** Saat melakukan merge tiga branch fitur (`feat/skills-section`, `feat/experience-section`, `style/interactive-navigation`) ke `master`, terjadi merge conflict pada `templates/index.html` dan `static/css/style.css`. AI yang menyarankan strategi merge `--no-ff` ternyata tidak memperhitungkan bahwa branch yang diedit di area file yang sama akan otomatis konflik. Saya harus resolve conflict secara manual dengan melihat marker `<<<<<<<` dan menggabungkan versi yang benar. Ini menunjukkan bahwa AI bisa memberikan rekomendasi yang *kelihatannya benar* tapi kehilangan detail eksekusi di level bawah.

Pelajaran yang saya ambil: AI adalah alat bantu yang mempercepat eksplorasi dan mengurangi waktu menulis boilerplate, tapi **tidak menggantikan pemahaman mendalam** tentang kode, konvensi, dan konteks spesifik proyek. Untuk proyek dengan identitas personal seperti portofolio, sentuhan manusia tetap esensial.

---

### Tugas 1

1. **Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `<section>`, `<article>`, atau `<aside>`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat *static web*? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?**

   Ya, saya menggunakan elemen semantik HTML5 secara konsisten di seluruh halaman portofolio ini. Struktur utama halaman saya bangun dengan `<header>` (berisi brand dan navigasi), `<main>` (membungkus seluruh konten utama), beberapa `<section>` dengan `id` berbeda untuk setiap bagian logis (`#profile`, `#skills`, `#experience`), `<nav>` khusus untuk daftar tautan navigasi, `<article>` untuk item-item yang berdiri sendiri seperti kartu skill dan entry experience, serta `<footer>` di bagian bawah.

   Elemen semantik ini sangat membantu saya dalam tiga hal. Pertama, **hierarki halaman menjadi eksplisit** — tanpa harus menebak dari susunan `<div>` bersarang, pembaca layar dan mesin pencari langsung tahu peran setiap blok. Kedua, **styling jadi lebih terarah** — saya bisa menargetkan bagian tertentu lewat tag selector tanpa harus menambahkan class berlebihan. Ketiga, **pemeliharaan lebih mudah** — ketika ingin menambah section baru (misalnya Projects di Tugas berikutnya), saya cukup membuat `<section id="projects">` baru tanpa mengubah struktur yang sudah ada. Tanpa elemen semantik, kode saya akan penuh `<div class="...">` generik yang membuat hubungan antar bagian menjadi ambigu dan sulit di-maintain.

2. **Ketika Anda mengatur CSS Anda agar tetap *responsive*, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?**

   Tantangan utama yang saya temukan adalah **menyusun ulang prioritas visual pada layar sempit**. Layout hero di desktop menggunakan grid dua kolom dengan foto di sisi kanan, tapi di mobile (lebar ≤ 600px) kolom itu menjadi terlalu rapat dan teks tertekan. Saya harus memutuskan: apakah foto tetap di atas (sebelum bio) atau pindah ke bawah? Saya memilih foto di atas dengan urutan `identity → photo → details` di mobile, karena nama dan foto adalah *first impression* yang paling penting untuk dikenali.

   Untuk section Skills yang awalnya tiga kolom berdampingan, di mobile saya ubah menjadi satu kolom penuh supaya setiap kartu tidak terpotong. Pada section Experience yang menggunakan grid dua kolom (meta di kiri, konten di kanan), di mobile saya stack menjadi satu kolom dengan `meta` di atas `content`, karena label period dan role lebih pendek dari deskripsi dan lebih cocok sebagai konteks pembuka.

   Evaluasi yang saya pakai cukup sederhana: saya membayangkan konten di viewport kecil sebagai **aliran linear** yang dibaca dari atas ke bawah. Elemen yang paling informatif (nama, judul, periode) harus muncul lebih dulu, sementara detail deskriptif mengikuti. Media query di CSS saya tulis dengan `max-width: 600px` sebagai breakpoint utama karena itu ukuran umum smartphone entry-level, dan saya tambahkan `scroll-margin-top: 80px` supaya anchor navigation tidak tertutup header sticky saat berpindah section.

3. **Website yang Anda buat saat ini adalah *static web* murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?**

   Batasan utama yang saya rasakan adalah **setiap perubahan konten membutuhkan pengeditan HTML secara manual**. Misalnya, untuk menambah satu skill baru di section Skills, saya harus membuka file `templates/index.html`, menyalin struktur `<article class="skill-card">` yang persis sama, lalu menuliskan judul dan isian ulang. Tidak ada cara untuk menambah data melalui antarmuka admin tanpa menyentuh kode. Begitu pula dengan section Experience — untuk menambahkan entry pengalaman baru, prosesnya identik: salin `<article class="timeline-item">`, isi ulang meta dan konten, simpan, commit, push. Repetitif dan rentan typo jika dilakukan sering.

   Batasan kedua adalah **tidak ada personalisasi berdasarkan pengunjung**. Portofolio ini sama untuk semua orang, padahal idealnya saya bisa menampilkan proyek berbeda untuk recruiter versus teman sebaya, atau menyembunyikan detail internal dari publik. Saat ini semua orang melihat konten yang sama persis.

   Untuk iterasi selanjutnya, dua fungsionalitas dinamis yang paling ingin saya tambahkan adalah: pertama, **penyimpanan data via database** (PostgreSQL dengan Django ORM) sehingga daftar skills, experience, dan projects bisa dikelola lewat Django Admin tanpa edit HTML. Schema-nya akan mengikuti struktur section yang sudah ada (`Skill`, `Experience`, `Project` sebagai model). Kedua, **form kontak yang benar-benar mengirim pesan**, bukan sekadar `mailto:` yang bergantung pada aplikasi email pengunjung. Form ini akan menyimpan pesan ke database dan (opsional) mengirim email notifikasi ke saya saat ada pesan baru. Keduanya sesuai dengan arsitektur MVT Django yang akan diajarkan di tutorial-tugas berikutnya, sehingga menjadi landasan yang baik untuk transisi dari static web ke dynamic web.
