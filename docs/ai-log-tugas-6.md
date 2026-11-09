# AI Log — Tugas 6 (Django REST Framework)

## Metadata

| Kolom | Nilai |
|---|---|
| Session | `local-d30772a71243797c9c…` |
| Judul sesi | Instruksi mengerjakan tugas-6.pdf |
| Model | z-ai/glm-5.3-flash |
| Periode (WIB) | 03 Nov 2026 10:20 – 09 Nov 2026 11:17 |
| Jumlah prompt unik | 7 (dari 7 baris user di store, hasil dedupe replikasi context compression) |
| Repo | github.com/fikrioktos/myportofolio |

Pembagian kerja: saya menjalankan seluruh perintah `git`, `manage.py`, dan pengujian; AI membaca spesifikasi tugas, mengusulkan snippet dan langkah kerja, serta menjalankan verifikasi read-only (`check`, test suite, grep) dan audit rubrik.

## Indeks Prompt

| # | Waktu (WIB) | Prompt |
|---|---|---|
| 1 | 03 Nov 2026 10:20 | bantu gw kerjain @file:`tugas-6.pdf` dong, bikinin instruksi buat gw kerjain kayak tutorial  --- Attached Context ---  📎 @file:`tugas-6.pdf` (application/pdf, 1 …(dipotong, asli 421 karakter) |
| 2 | 07 Nov 2026 08:36 | udah gw kerjain nih, bantu cek dong |
| 3 | 08 Nov 2026 10:29 | udah gw benerin, bantu cek lagi dong |
| 4 | 08 Nov 2026 15:54 | udah aman kan? bantu evaluasi kerjaan gw menurut rubrik dong |
| 5 | 08 Nov 2026 16:06 | coba bantu cek lagi sebelum gw commit |
| 6 | 09 Nov 2026 11:08 | coba cek lagi, gw emang belum commit apa2 sih |
| 7 | 09 Nov 2026 11:17 | gw butuh ai log nya nih, bikinin dong buat sesi ini biar gw bisa masukin |

## Kutipan Prompt & Jawaban

### 1. 03 Nov 2026 10:20

**Prompt:**

> bantu gw kerjain @file:`tugas-6.pdf` dong, bikinin instruksi buat gw kerjain kayak tutorial
> 
> --- Attached Context ---
> 
> 📎 @file:`tugas-6.pdf` (application/pdf, 144.0 KB) — binary file, not inlined as text. It is available on disk at `C:\Users\Fikri\Code\PBP\tugas-6.pdf`. Use your tools to work with it (read or convert it, extract its text, or view/render it as needed); do not tell the user the file type is unsupported.

**Jawaban (ringkas):**

> Oke, gw baca spek-nya dan cek kondisi repo. Dari PDF, Tugas 6 nerapin pola DRF Tutorial 07 ke bagian Tugas 3–5 kamu, yaitu **Experience** (Tugas 3 form/update, Tugas 4 role Editor, Tugas 5 AJAX). Deadline: **Senin 9 November 2026, 23.59 WIB**. Tutorial 07 harus kelar dulu, deadline-nya **Rabu 4 November**, besok.
> 
> ## Kondisi repo sekarang
> 
> - Branch aktif `feat/api-drf`, commit `13fb337` sudah ada di `origin/feat/api-drf`. Belum di-merge ke `master`, dan `pws/master` ketinggalan 1 commit.
> - `mana …(dipotong, asli 5185 karakter)


### 2. 07 Nov 2026 08:36

**Prompt:**

> udah gw kerjain nih, bantu cek dong

**Jawaban (ringkas):**

> Check lolos. Test suite-nya makan waktu lebih dari 3 menit, jadi gw jalanin ulang dengan timeout lebih panjang sambil baca diff-nya.


### 3. 08 Nov 2026 10:29

**Prompt:**

> udah gw benerin, bantu cek lagi dong

**Jawaban (ringkas):**

> Route lama sudah hilang dan `check` bersih. Sekarang jalanin test suite penuh, yang butuh sekitar 5 menit.


### 4. 08 Nov 2026 15:54

**Prompt:**

> udah aman kan? bantu evaluasi kerjaan gw menurut rubrik dong

**Jawaban (ringkas):**

> Gw cek ulang kondisi repo dulu, jangan pakai hasil sesi sebelumnya.


### 5. 08 Nov 2026 16:06

**Prompt:**

> coba bantu cek lagi sebelum gw commit

**Jawaban (ringkas):**

> Poin perbaikan dari sesi sebelumnya belum ada yang berubah: `api/experience/` masih terdaftar. Gw cek sisa itu dan jalanin suite lagi.


### 6. 09 Nov 2026 11:08

**Prompt:**

> coba cek lagi, gw emang belum commit apa2 sih

**Jawaban (ringkas):**

> Lu belum commit apa pun. Commit terakhir masih `13fb337` dari sesi sebelumnya, dan HEAD sama dengan `origin/feat/api-drf`.
> 
> Yang sudah ada di index (staged, belum dikomit):
> - `main/urls.py`: penghapusan 32 baris (route experience lama)
> - `main/views.py`: penghapusan 159 baris (view experience lama, tapi juga staged parsial, sisanya belum)
> - `templates/components/experience_delete_modal.html`: dihapus
> - `templates/experience_form.html`: dihapus
> 
> Yang masih unstaged (modifikasi di working tree):
> - …(dipotong, asli 1502 karakter)


### 7. 09 Nov 2026 11:17

**Prompt:**

> gw butuh ai log nya nih, bikinin dong buat sesi ini biar gw bisa masukin

**Jawaban (ringkas):**

> Sesuai prosedur di skill, gw ambil log dari session store langsung (bukan export bawaan yang kepotong compression). Pertama, cari session id sesi ini.

---

## Tools dan Model

- Tools: Hermes Agent (desktop), dengan akses terminal (git-bash), read/patch/write file, dan pencarian file. AI tidak pernah push ke remote; commit dijalankan user.
- Model: z-ai/glm-5.3-flash

## Strategi Prompting

- Prompt dibuat bertahap per langkah: baca spek dulu, lalu cek repo, lalu usulkan langkah, lalu user yang menjalankan git dan manage.py.
- Setiap klaim faktual diminta diverifikasi ulang dengan perintah (`git status`, `grep`, `manage.py check`, `manage.py test`) sebelum dipercaya, bukan dari ingatan sesi sebelumnya.
- Perubahan kode hanya dilakukan setelah persetujuan eksplisit di giliran yang sama ("gas", "langsung", "gas commit").

## Bagian yang Dibantu AI

- Membaca dan merangkum spek Tugas 6 dari PDF, termasuk daftar kriteria rubrik.
- Mengusulkan desain: pindah halaman Experience ke `/api/v1/experiences/`, satu modal untuk tambah dan ubah, kode akses dihapus, `@ensure_csrf_cookie` di `show_experience`.
- Menulis ulang `static/js/experience.js` dan `templates/components/experience_form_modal.html`, lalu user meninjau dan menerimanya.
- Menulis test tambahan di `main/tests_api.py` (owner, validasi, CSRF, anonim) dan `ExperienceRoleRenderTest` di `main/tests.py`.
- Menyusun draft bagian README Tugas 6 dan memisahkan perubahan per commit.

## Keterbatasan AI yang Ditemukan

- **Klaim git salah.** AI pernah menyatakan index "sudah bersih" dan "grup refactor sudah siap", padahal `git diff --cached` masih campur. User yang menangkap ini.
- **Klaim yang tidak dicek ke spek.** AI menulis bahwa `/api/experience/` dan `/xml/` "wajib Tutorial 03", tanpa membuka spek. User menunjukkan spek tidak memintanya dihapus, dan README dikoreksi ke alasan "endpoint baca".
- **Hitungan dari ingatan.** Jumlah test di README sempat salah (70, 93, 76). Setelah itu jumlah dihitung dengan `grep -c "def test_"` per file dan diverifikasi dengan `manage.py test main` (77 OK).
- **Urutan commit tidak diuji.** Usulan pertama memisahkan penghapusan view ke commit yang sama dengan integrasi. Snapshot `check` menunjukkan `ImportError` (`create_experience` masih di-import `urls.py`), jadi penghapusan view dipindah ke commit refactor bersama `urls.py`.
- **Tidak bisa melihat browser.** Modal tambah, ubah, hapus, dan star belum diuji di browser. Semua klaim UI berbasis test client dan pembacaan HTML, bukan tampilan nyata.

## Perbaikan Manual oleh User

- Menangkap jumlah test yang salah di README dan meminta hitungan per file.
- Menolak klaim "endpoint lama wajib" dan meminta alasannya dikoreksi di README.
- Meminta test anonim (POST, PATCH, DELETE) dengan pengecekan isi database, lalu test itu ditambahkan.
- Menangkap staging yang campur dan memberi urutan commit per fitur.
- Menjalankan semua perintah `git commit`.

## Status Log

- Prompt 7 terpotong di tengah jawaban. Kelanjutan sesi belum diambil dari session store.
- Jawaban di log bersifat ringkasan (`(ringkas)`), bukan transkrip utuh.
