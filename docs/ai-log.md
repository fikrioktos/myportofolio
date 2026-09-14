# Log Penggunaan AI — Tugas 2 (PBP)

Log prompting pengerjaan Tugas 2: percakapan saya dengan AI agent (Hermes Agent),
disusun dari riwayat sesi asli. Prompt dikutip apa adanya, tanpa diedit.

| | |
|---|---|
| Sesi | `20260913_192654_8f87b1` |
| Model | `deepseek-flash` (13–14 Sep pagi) → `glm-5.3-flash` (14 Sep siang) |
| Periode | 13 Sep 2026, 19:27 WIB — 14 Sep 2026, 13:52 WIB |
| Jumlah prompt | 31 |
| Repo | https://github.com/fikrioktos/myportofolio |

**Pola kerja:** AI berperan sebagai pemandu dan reviewer. Saya yang menjalankan seluruh
`makemigrations`, `migrate`, `runserver`, dan perintah `git`; AI membaca spesifikasi,
mengusulkan potongan kode, lalu menjalankan verifikasi read-only (test, cek isi DB).
Setiap perubahan kode saya review dulu sebelum commit.

## Daftar prompt

| # | Waktu | Prompt |
|---|---|---|
| 1 | 13 Sep 2026, 19:27 WIB | bantu gw kerjain tugas 2 dong, rencananya gw mau nambah model projects |
| 2 | 13 Sep 2026, 19:37 WIB | gw udah sampe 1c, buat migration tingga makemigrations terus migrate kan? abis itu buat masukin datanya biar gw aja manual lewat shell |
| 3 | 13 Sep 2026, 19:39 WIB | gw ga mau dua kali sih, kayaknya mending langsung migrate buat dua-duanya. Sekarang gw makemigrations sama migrate dulu ya |
| 4 | 13 Sep 2026, 19:41 WIB | tolong add dong seedsnya, gw udah migrate tadi |
| 5 | 13 Sep 2026, 19:43 WIB | test dulu ga sih di local sebelum commit? |
| 6 | 13 Sep 2026, 19:45 WIB | kok pas gw run server di local ga ada page projectsnya ya |
| 7 | 13 Sep 2026, 19:46 WIB | emang udah safe to commit ya buat branch projects model? |
| 8 | 13 Sep 2026, 19:48 WIB | warning: in the working copy of 'main/migrations/0005_seed_project_data.py', LF will be replaced by CRLF the next time Git touches it  M main/admin.py  A main/m …(dipotong, asli 785 karakter) |
| 9 | 13 Sep 2026, 19:50 WIB | Switched to branch 'master'  Your branch is up to date with 'origin/main'.  Merge made by the 'ort' strategy.   main/admin.py \| 16 ++++++-   main/migrations/000 …(dipotong, asli 570 karakter) |
| 10 | 13 Sep 2026, 19:53 WIB | ga ada cardnya, sama kedua projects kompetisi apus aja @image:C:\Users\fikri\AppData\Roaming\Hermes\composer-images\image_6851ab.png |
| 11 | 13 Sep 2026, 20:01 WIB | oke udah gw commit, runserver juga aman. Lanjut step 3 langsung eksekusi aja |
| 12 | 13 Sep 2026, 22:40 WIB | coba kita evaluasi dulu checklist nya tugas sejauh ini gimana |
| 13 | 13 Sep 2026, 22:58 WIB | cek rubrik juga dong apa yang masih kurang |
| 14 | 13 Sep 2026, 23:08 WIB | kayaknya sebelum rapihin .md gw mau nambahin beberapa aspek kreativitas dulu. Gw mikir buat experiences kayak bisa dibagi dua lagi antara kepanitian dan organis …(dipotong, asli 235 karakter) |
| 15 | 14 Sep 2026, 10:15 WIB | kayaknya adjustment yang gw usulin masih berlebihan buat tugas 2 ini, mungkin kita coba adjustment yang lebih simple lagi tapi tetep significant |
| 16 | 14 Sep 2026, 10:41 WIB | buat projects gw ada hal yang bisa di attach sih, kayak game visual novel gw bisa attach laporan dan deployment game nya, buat project rag juga gw bisa kasih te …(dipotong, asli 331 karakter) |
| 17 | 14 Sep 2026, 10:50 WIB | buat bem itu bem fasilkom btw, ini link nya @url:`https://bem.cs.ui.ac.id/` link deployment game: @url:`https://rifkypadjri.itch.io/final-project-mpkt` buat tec …(dipotong, asli 3011 karakter) |
| 18 | 14 Sep 2026, 11:02 WIB | technical report : @url:`https://drive.google.com/file/d/1UZNI35qsRv67pJMzDqqqyKOk7OYu6shq/view?usp=sharing` laporan VN : @url:`https://drive.google.com/file/d/ …(dipotong, asli 19738 karakter) |
| 19 | 14 Sep 2026, 11:09 WIB | gw lanjut merge ya |
| 20 | 14 Sep 2026, 11:12 WIB | udah gw merge dan bikin branch baru, langsung aja adjust code modelsnya |
| 21 | 14 Sep 2026, 11:15 WIB | udah gw migrate |
| 22 | 14 Sep 2026, 11:22 WIB | udah gw migrate dan cek datanya |
| 23 | 14 Sep 2026, 11:27 WIB | gapapa langsung edit aja file nya |
| 24 | 14 Sep 2026, 11:36 WIB | udah gw check, runserver udah oke, commit juga udah |
| 25 | 14 Sep 2026, 13:08 WIB | README biar gw aja, itu belom gw commit btw. |
| 26 | 14 Sep 2026, 13:10 WIB | merge dulu aja ga sih baru nulis readme |
| 27 | 14 Sep 2026, 13:13 WIB | gw mau push dulu aja semua commit yang belum dipush, nanti readme gampang di push terpisah |
| 28 | 14 Sep 2026, 13:17 WIB | sekarang review checklist dan rubrik dulu |
| 29 | 14 Sep 2026, 13:21 WIB | session ini bisa gw export ke JSON kan sih, kayaknya mending gitu aja |
| 30 | 14 Sep 2026, 13:30 WIB | oke nanti gw minta tolong buatin lagi log nya, berarti di luar dokementasi dan reflektif menurut rubrik udah oke belom kerjaan gw |
| 31 | 14 Sep 2026, 13:52 WIB | tugas refleksi udah gw kerjain, detail2 di readme juga udah gw update. Sanity check terakhir kali dong abis itu bikinin log buat session ini |

---

## Kutipan pertukaran

### 1. 13 Sep 2026, 19:27 WIB

**Prompt saya:**

> bantu gw kerjain tugas 2 dong, rencananya gw mau nambah model projects

**Tanggapan AI (kutipan):**

> Udah gw baca spek `tugas-2.txt`, kondisi repo, dan semua file yang relevan. Ini dulu petaannya sebelum kita ngoding:
> **Status Tugas 2 sekarang**
> | Checklist spek | Status |
> |---|---|
> | Model baru (3+ field selain PK) | ❌ belum |
> | Migrasi dibuat & di-commit | ❌ |
> | View + context + template baru | ❌ |
> | Loop `{% for %}` + `{% empty %}` | ❌ |
> | Halaman sendiri, beda dari `/` | ❌ |
> | Named route di `main/urls.py` | ❌ | …(dipotong, asli 1998 karakter)

### 2. 13 Sep 2026, 19:37 WIB

**Prompt saya:**

> gw udah sampe 1c, buat migration tingga makemigrations terus migrate kan? abis itu buat masukin datanya biar gw aja manual lewat shell

**Tanggapan AI (kutipan):**

> Ya, betul — `makemigrations` dulu (bikin file migrasi dari perubahan `models.py`), baru `migrate` (jalanin + ubah skema DB):
> ```bash
> env/Scripts/python manage.py makemigrations main
> env/Scripts/python manage.py migrate
> ```
> Output `makemigrations` harusnya `Create model Project` → `main/migrations/0004_project.py`. Kalau dia bilang `No changes detected`, berarti file `models.py` belum ke-save.
> ### Masukin data lewat s …(dipotong, asli 3276 karakter)

### 3. 13 Sep 2026, 19:39 WIB

**Prompt saya:**

> gw ga mau dua kali sih, kayaknya mending langsung migrate buat dua-duanya. Sekarang gw makemigrations sama migrate dulu ya

**Tanggapan AI (kutipan):**

> Oke gas. Perlu dilurusin dikit: jalanin `migrate` dua kali itu **normal dan bukan "dua kali kerja"** — `migrate` cuma ngecek migrasi mana yang belum pernah diterapkan di DB, jadi panggilan kedua setelah 0005 ada tinggal nerapin 0005 doang. Yang jadi masalah justru kalau lo input data dua cara (shell + migrasi).
> Jadi urutannya:
> **1. Sekarang (yang lagi lo jalanin):**
> ```bash
> env/Scripts/python manage.py makemigrations …(dipotong, asli 2145 karakter)

### 4. 13 Sep 2026, 19:41 WIB

**Prompt saya:**

> tolong add dong seedsnya, gw udah migrate tadi

**Tanggapan AI (kutipan):**

> File-nya udah gw tulis: `main/migrations/0005_seed_project_data.py`. Verifikasi yang gw jalanin (read-only):
> - `makemigrations --check --dry-run` → **No changes detected** (file migrasi ini gak nyimpang dari state model, aman)
> - `migrate --plan` → **`main.0005_seed_project_data` — Raw Python operation** (kebaca, dependensinya ke `0004_project` resolve, dan belum diterapkan)
> Sekarang bagian lo:
> ```bash
> env/Scripts/pyt …(dipotong, asli 1326 karakter)

### 5. 13 Sep 2026, 19:43 WIB

**Prompt saya:**

> test dulu ga sih di local sebelum commit?

**Tanggapan AI (kutipan):**

> Gw baru jalanin dua-duanya buat ngasih jawaban jujur:
> - `manage.py check` → **System check identified no issues** ✅
> - `manage.py test main` → **masih `FAILED (errors=6)`** — tapi cek dulu akar errornya: keenamnya mati di baris yang sama, `IntegrityError: NOT NULL constraint failed: main_experience.started_at`. Itu dari `setUp()` di `tests.py` yang bikin Experience tanpa `started_at`, alias **warisan dari Tutorial 2** …(dipotong, asli 1889 karakter)

### 6. 13 Sep 2026, 19:45 WIB

**Prompt saya:**

> kok pas gw run server di local ga ada page projectsnya ya

**Tanggapan AI (kutipan):**

> Ketemu sebabnya — halaman `/projects/` **belum pernah dibikin**. Yang udah ada baru lapisan data: gw cek DB lokal lo sekarang, `0001`–`0005` semua udah ter-apply dan `main_project` isi **4 baris** (Visual Novel, RAG, Kaggle, Website Portofolio). Jadi model + migrasi + datanya udah beres.
> Tapi `main/urls.py` masih cuma punya dua route (`""` dan `"experience/"`), belum ada view `show_projects`, belum ada `templates/pro …(dipotong, asli 8231 karakter)

### 7. 13 Sep 2026, 19:46 WIB

**Prompt saya:**

> emang udah safe to commit ya buat branch projects model?

**Tanggapan AI (kutipan):**

> Ya, aman. Gw verifikasi dulu isi working tree-nya, bukan cuma percaya:
> **1. Diff-nya persis sebatas yang direncanain**
> - `main/models.py` → **+25 baris**, isinya cuma class `Project` (gak ada baris `Experience` yang kesenggol)
> - `main/admin.py` → **+16 / −1**, komentar placeholder `# Register your models here.` diganti dua `@admin.register`
> - Untracked: cuma `0004_project.py` dan `0005_seed_project_data.py`. Gak ada …(dipotong, asli 2320 karakter)

### 8. 13 Sep 2026, 19:48 WIB

**Prompt saya:**

> warning: in the working copy of 'main/migrations/0005_seed_project_data.py', LF will be replaced by CRLF the next time Git touches it 
> M main/admin.py 
> A main/migrations/0004_project.py 
> A main/migrations/0005_seed_project_data.py 
> M main/models.py 
>  main/admin.py | 16 ++++++- 
>  main/migrations/0004_project.py | 27 +++++++++++ 
>  main/migrations/0005_seed_project_data.py | 75 +++++++++++++++++++++++++++++++ 
>  main/models.py | 26 +++++++++++ 
>  4 files changed, 143 insertions(+), 1 deletion(-) 
> [feat/projects-model 4a771b4] feat(projects): tambah model Project beserta migrasi dan data awal 
>  4 files changed, 143 insertions(+), 1 deletion(-) 
>  create mode 100644 main/migrations/0004_project.py 
>  create mode 100644 main/migrations/0005_seed_project_data.py
> ada yang concerning ga?

**Tanggapan AI (kutipan):**

> Verdict: **gak ada yang concerning.** Dua-duanya kosmetik. Rinciannya:
> **1. Warning `LF will be replaced by CRLF` — aman, jangan diapa-apain**
> Penyebabnya setting Git lo `core.autocrlf=true` (gw cek: outputnya `true`). Artinya Git **nyimpen LF di repo**, tapi ngasih CRLF di working copy Windows. Warning itu cuma bilang: "file ini di disk lo LF, nanti kalau gw sentuh lagi bakal gw jadiin CRLF."
> Yang penting isi di rep …(dipotong, asli 2711 karakter)

### 9. 13 Sep 2026, 19:50 WIB

**Prompt saya:**

> Switched to branch 'master' 
> Your branch is up to date with 'origin/main'. 
> Merge made by the 'ort' strategy. 
>  main/admin.py | 16 ++++++- 
>  main/migrations/0004_project.py | 27 +++++++++++ 
>  main/migrations/0005_seed_project_data.py | 75 +++++++++++++++++++++++++++++++ 
>  main/models.py | 26 +++++++++++ 
>  4 files changed, 143 insertions(+), 1 deletion(-) 
>  create mode 100644 main/migrations/0004_project.py 
>  create mode 100644 main/migrations/0005_seed_project_data.py 
> Switched to a new branch 'feat/projects-page'
> aman kan ya? buat step 2 gw serahin full ke lo deh

**Tanggapan AI (kutipan):**

> Sip, merge-nya bener. Gw verifikasi dulu + intip satu-dua file biar edit-nya pas:

### 10. 13 Sep 2026, 19:53 WIB

**Prompt saya:**

> ga ada cardnya, sama kedua projects kompetisi apus aja
> @image:C:\Users\fikri\AppData\Roaming\Hermes\composer-images\image_6851ab.png

**Tanggapan AI (kutipan):**

> Kartunya gak muncul padahal CSS-nya udah ke-load — itu pola khas **CSS basi**. Gw cek dulu file mana yang beneran disajiin:

### 11. 13 Sep 2026, 20:01 WIB

**Prompt saya:**

> oke udah gw commit, runserver juga aman. Lanjut step 3 langsung eksekusi aja

**Tanggapan AI (kutipan):**

> Semua commit lo udah masuk, tree bersih. Gw tulis ulang `main/tests.py`:

### 12. 13 Sep 2026, 22:40 WIB

**Prompt saya:**

> coba kita evaluasi dulu checklist nya tugas sejauh ini gimana

**Tanggapan AI (kutipan):**

> Gw evaluasi pakai bukti, bukan ingatan — jadi gw periksa langsung ke repo:

### 13. 13 Sep 2026, 22:58 WIB

**Prompt saya:**

> cek rubrik juga dong apa yang masih kurang

**Tanggapan AI (kutipan):**

> Gw bandingin kondisi repo sekarang sama tiap tingkat di rubrik. Angka band-nya **estimasi gw**, bukan vonis — tapi tiap klaim di bawah ada dasar file/barisnya.
> ## 1. Fungsionalitas & Kesesuaian Topik (70%)
> **Estimasi sekarang: 3.5** — semua checklist spek kena akurat (id 1–9 di tabel tadi), gak ada bug.
> Yang masih kurang buat **4** ("melampaui ekspektasi, bebas berkreasi"):
> | Gap | Catatan |
> |---|---|
> | Belum ada hal …(dipotong, asli 1256 karakter)

### 14. 13 Sep 2026, 23:08 WIB

**Prompt saya:**

> kayaknya sebelum rapihin .md gw mau nambahin beberapa aspek kreativitas dulu. Gw mikir buat experiences kayak bisa dibagi dua lagi antara kepanitian dan organisasi, terus mungkin bisa ditambahin logo dan dokumentasi dari experiences gw

**Tanggapan AI (kutipan):**

> Ini perubahan scope yang cukup gede, jadi gw periksa dulu apa yang udah ada di repo sebelum nyaranin bentuk modelnya — terutama soal **gambar di production**, itu bagian yang paling gampang bikin deploy jebol.

### 15. 14 Sep 2026, 10:15 WIB

**Prompt saya:**

> kayaknya adjustment yang gw usulin masih berlebihan buat tugas 2 ini, mungkin kita coba adjustment yang lebih simple lagi tapi tetep significant

**Tanggapan AI (kutipan):**

> Lo benar, dan gw salah arah — gw nambahin tiga fitur (field baru + pengelompokan + galeri) padahal ekspektasi lo cuma "satu tambahan yang berarti". Gw cek dulu isi kartu Projects biar usulan barunya berdasar, bukan ngarang.

### 16. 14 Sep 2026, 10:41 WIB

**Prompt saya:**

> buat projects gw ada hal yang bisa di attach sih, kayak game visual novel gw bisa attach laporan dan deployment game nya, buat project rag juga gw bisa kasih technical reportnya. Buat experience mungkin gw bisa kasih link ke profile kepanitian atau organisasinya? kayak ristek ya ke web ristek, ddp0 ke ddp0, dan ta ke web fasilkom

**Tanggapan AI (kutipan):**

> Ini justru jawaban yang lebih baik dari usulan gw — lo punya konten nyata, bukan cuma ide bentuk. Dan bentuknya jauh lebih simpel: **cuma nambah field link, nol halaman baru, nol template baru.**
> Gw cek dulu URL-nya beneran ada apa nggak, biar gw nggak ngarang alamat:

### 17. 14 Sep 2026, 10:50 WIB

**Prompt saya:**

> buat bem itu bem fasilkom btw, ini link nya
> @url:`https://bem.cs.ui.ac.id/`
> link deployment game: @url:`https://rifkypadjri.itch.io/final-project-mpkt`
> buat technical report gw masih ada projects overleaf nya, mending upload ke drive aja kah?
> --- Context Warnings ---
> - @url:`https://rifkypadjri.itch.io/final-project-mpkt`: no content extracted
> --- Attached Context ---
> 🌐 @url:`https://bem.cs.ui.ac.id/` (658 tokens)
> ![bem-logo](https://bem.cs.ui.ac.id/_next/image?url=%2Flogo%2Fbem-text.png&w=640&q=75)
> ###### Beranda
> ###### Tentang Kami
> ###### Acara
> ###### Tautan Penting
> [**Berikan feedback**](https://www.instagram.com/bemfasilkomui/?hl=en)
> ![about-fasilkom](https://bem.cs.ui.ac.id/homepage/gaung.svg)
> ## Tentang Fasilkom UI
> "Fakultas Ilmu Komputer Universitas Indonesia (Fasilkom UI) adalah tempat yang menantang orang-orang dengan rasa ingin tahu yang tinggi dan bersemangat untuk berimajinas …(dipotong, asli 3011 karakter)

**Tanggapan AI (kutipan):**

> Dua link lo gw cek — **dua-duanya hidup**: `bem.cs.ui.ac.id` → `200`, dan itch.io-nya → `200` dengan judul "FINAL_PROJECT_MPKT by rifkypadjri" (dan itu **bisa dimainkan langsung di browser**, nilai plus buat portofolio).
> Dan lo bener soal BEM — gw yang salah nyari tadi: BEM **UI** (tingkat universitas) beda dari **BEM Fasilkom UI**. Yang lo maksud jelas yang kedua.
> Buat pertanyaan Overleaf vs Drive, gw cek aturan sha …(dipotong, asli 462 karakter)

### 18. 14 Sep 2026, 11:02 WIB

**Prompt saya:**

> technical report : @url:`https://drive.google.com/file/d/1UZNI35qsRv67pJMzDqqqyKOk7OYu6shq/view?usp=sharing`
> laporan VN : @url:`https://drive.google.com/file/d/1UtcfWXjAXR13z_E-YprtPqSUsl-TmXf5/view?usp=sharing`
> --- Attached Context ---
> 🌐 @url:`https://drive.google.com/file/d/1UZNI35qsRv67pJMzDqqqyKOk7OYu6shq/view?usp=sharing` (3918 tokens)
> ## Ketika RAG Gagal, Siapa yang Salah?
> *Diagnosis Kualitas Retrieval pada Sistem RAG Berbahasa Indonesia*
> # DSAI Internal Project — NLP Track
> # Proyek 4: RAG Retrieval Quality Diagnosis
> Anggota Tim:
> Aldo
> Opang
> Okto
> Dataset: TyDi QA Indonesian (Google Research)
> Model LLM: Gemma-3-27B-IT (via Gemini API)
> Retriever: BM25 (rank_bm25) + Semantic
> (paraphrase-multilingual-MiniLM-L12-v2)
> April 2026
> ---
> ## Ringkasan
> Retrieval-Augmented Generation (RAG) adalah arsitektur populer yang menggabungkan retriever dan large language model (LLM). Ketika jawaban RAG
> sal …(dipotong, asli 19738 karakter)

**Tanggapan AI (kutipan):**

> Dua link Drive lo **kebaca publik** — technical report RAG (sampai 18.6k karakter kebaca) dan laporan VN (`TugasAkhir_FG2_MPKTF.pdf`, 14 halaman). Tapi gw nemu satu hal yang perlu lo konfirmasi. Gw cek dulu:

### 19. 14 Sep 2026, 11:09 WIB

**Prompt saya:**

> gw lanjut merge ya

**Tanggapan AI (kutipan):**

> Oke, ini perintahnya — dari posisi lo sekarang (di `feat/projects-page`, 4 commit di depan `master`):
> ```bash
> cd "C:/Users/fikri/Code/PBP/myportofolio"
> git switch master
> git merge --no-ff feat/projects-page -m "merge: halaman Projects dan perbaikan test ke master"
> ```
> **Kenapa `--no-ff`:** tanpa itu, Git bakal fast-forward (master cuma maju nutupin branch tanpa jejak merge). Dengan `--no-ff`, terbentuk merge commit y …(dipotong, asli 1042 karakter)

### 20. 14 Sep 2026, 11:12 WIB

**Prompt saya:**

> udah gw merge dan bikin branch baru, langsung aja adjust code modelsnya

**Tanggapan AI (kutipan):**

> Model kelar. Sekarang gw verifikasi edit-nya koheren (read-only, nggak nulis apa-apa):

### 21. 14 Sep 2026, 11:15 WIB

**Prompt saya:**

> udah gw migrate

**Tanggapan AI (kutipan):**

> 0007 udah masuk, kolomnya udah ada di dua tabel, dan gw udah konfirmasi **judul baris yang ada** biar migrasi datanya ngena ke baris yang bener (bukan bikin baris baru). Sekarang migrasi data:

### 22. 14 Sep 2026, 11:22 WIB

**Prompt saya:**

> udah gw migrate dan cek datanya

**Tanggapan AI (kutipan):**

> Data lengkap dan bener semua — 4 Experience punya `organization_url`, VN punya report + deployment, RAG punya report, dan `0008` udah kecatet diterapkan. Sekarang gw lihat CSS-nya dulu biar link barunya nyatu sama gaya yang udah ada:

### 23. 14 Sep 2026, 11:27 WIB

**Prompt saya:**

> gapapa langsung edit aja file nya

**Tanggapan AI (kutipan):**

> Template + CSS kelar. Sekarang test-nya:

### 24. 14 Sep 2026, 11:36 WIB

**Prompt saya:**

> udah gw check, runserver udah oke, commit juga udah

**Tanggapan AI (kutipan):**

> Rapi — 4 commit di `feat/external-links`, merge commit `1e86ed3` udah ada di master, working tree bersih. Sekarang gw baca README dan spek Tugas 2 biar jawabannya ngena ke pertanyaan yang diminta:

### 25. 14 Sep 2026, 13:08 WIB

**Prompt saya:**

> README biar gw aja, itu belom gw commit btw.

**Tanggapan AI (kutipan):**

> Oke, gw nggak sentuh README. Status barusan: branch `feat/external-links`, `git status` **bersih**, dan `git diff README.md` **kosong** — jadi semua commit fitur lo udah masuk, README masih versi lama.
> Satu keputusan kecil yang perlu lo tentuin sekarang: **README lo commit di branch mana?** Paling simpel kerjain di branch ini (`feat/external-links`) bareng fiturnya, lalu merge sekali. Nggak perlu bikin `docs/` branch …(dipotong, asli 1890 karakter)

### 26. 14 Sep 2026, 13:10 WIB

**Prompt saya:**

> merge dulu aja ga sih baru nulis readme

**Tanggapan AI (kutipan):**

> Sebelum gw jawab, gw cek dulu apakah merge-nya bakal bersih (read-only, nggak gw jalanin merge-nya):

### 27. 14 Sep 2026, 13:13 WIB

**Prompt saya:**

> gw mau push dulu aja semua commit yang belum dipush, nanti readme gampang di push terpisah

**Tanggapan AI (kutipan):**

> Merge commit udah masuk (`b787b68`) dan branch fitur udah kepakai habis — nol di belakang master. Sebelum push, gw pastiin suite-nya masih hijau di `master`:

### 28. 14 Sep 2026, 13:17 WIB

**Prompt saya:**

> sekarang review checklist dan rubrik dulu

**Tanggapan AI (kutipan):**

> Curl yang terakhir keputus di tengah (grep nutup pipe-nya), jadi verifikasi deploy-nya belum lengkap. Gw ulang sambil sekalian cek klausa-klausa rubrik yang bisa gw buktiin:

### 29. 14 Sep 2026, 13:21 WIB

**Prompt saya:**

> session ini bisa gw export ke JSON kan sih, kayaknya mending gitu aja

**Tanggapan AI (kutipan):**

> Masuk akal — log mentah malah lebih jujur daripada ringkasan buatan gw. Gw cek dulu fitur export-nya ada apa nggak:

### 30. 14 Sep 2026, 13:30 WIB

**Prompt saya:**

> oke nanti gw minta tolong buatin lagi log nya, berarti di luar dokementasi dan reflektif menurut rubrik udah oke belom kerjaan gw

**Tanggapan AI (kutipan):**

> Udah oke, sisa dokumentasi doang. Rekap bukti yang udah gw verifikasi langsung barusan-barusan ini (bukan ingatan):
> **Fungsionalitas (70%)** ✅
> - Checklist spek 10/10: model `Project` 9 field + PK UUID, 5 migrasi ter-apply, view + template + named route, `{% for %}`/`{% empty %}`, zero hard-coded data di template
> - PWS live: `/`, `/experience/`, `/projects/` semua 200, **7 link eksternal ter-render di production** (ud …(dipotong, asli 1502 karakter)

### 31. 14 Sep 2026, 13:52 WIB

**Prompt saya:**

> tugas refleksi udah gw kerjain, detail2 di readme juga udah gw update. Sanity check terakhir kali dong abis itu bikinin log buat session ini

**Tanggapan AI (kutipan):**

> README-nya udah gw baca diff-nya utuh — reflektif lengkap, struktur update bagus. Tinggal dua verifikasi faktual sebelum kasih verdict:
