from datetime import date
import json
import uuid

from django.test import TestCase, override_settings
from django.urls import reverse

from main.models import Experience, Project

TEST_ACCESS_CODE = "kode-uji-portofolio"


class PortfolioTestCase(TestCase):
    """Data dasar yang dipakai bersama oleh test halaman-halaman portofolio.

    Database test dibangun dengan menjalankan seluruh migrasi, termasuk data
    migration seed (0003 dan 0005), sehingga baris seed ikut masuk ke sini.
    Baris tersebut dibersihkan dulu agar tiap test berdiri sendiri dan tidak
    bergantung pada isi data awal.
    """

    def setUp(self):
        Experience.objects.all().delete()
        Project.objects.all().delete()

        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            role="Teaching Assistant",
            organization="Fasilkom UI",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            started_at=date(2025, 8, 1),
        )
        self.project = Project.objects.create(
            title="Website Portofolio PBP",
            category="personal",
            description="Website portofolio berbasis Django dengan alur MVT.",
            technologies="Django, HTML5, CSS3",
            repository_url="https://github.com/fikrioktos/myportofolio",
            started_at=date(2026, 8, 31),
        )


class MainProfileTest(PortfolioTestCase):
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertNotContains(response, self.project.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)


class ExperienceTest(PortfolioTestCase):
    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.role)
        self.assertContains(response, self.experience.organization)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Present")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = date(2026, 6, 30)
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, str(self.experience.started_at.year))
        self.assertContains(response, str(self.experience.ended_at.year))
        self.assertNotContains(response, "Present")

    def test_experience_page_shows_organization_link(self):
        self.experience.organization_url = "https://bem.cs.ui.ac.id/"
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, self.experience.organization_url)

    def test_experience_without_organization_link(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertNotContains(response, "Kunjungi situs")


class ProjectTest(PortfolioTestCase):
    def test_project_model(self):
        self.assertEqual(str(self.project), "Website Portofolio PBP")
        self.assertEqual(self.project.get_category_display(), "Personal")
        self.assertTrue(self.project.is_ongoing)

    def test_projects_url_is_accessible(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_projects_page_shows_data(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.get_category_display())
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.project.technologies)
        self.assertContains(response, self.project.repository_url)
        self.assertContains(response, "Present")
        self.assertNotContains(response, self.experience.title)

    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

    def test_projects_page_shows_external_links(self):
        self.project.report_url = "https://drive.google.com/file/d/contoh/view"
        self.project.deployment_url = "https://contoh.itch.io/game"
        self.project.save()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, self.project.report_url)
        self.assertContains(response, self.project.deployment_url)

    def test_projects_without_external_links(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertNotContains(response, "Lihat laporan")
        self.assertNotContains(response, "Coba demo")


@override_settings(PORTFOLIO_ACCESS_CODE=TEST_ACCESS_CODE)
class ProjectFormTest(PortfolioTestCase):
    def test_create_project_url_is_accessible(self):
        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")

    def test_create_project_form_shows_fields(self):
        response = self.client.get(reverse("main:create_project"))

        for field in [
            "title",
            "category",
            "description",
            "technologies",
            "started_at",
            "access_code",
        ]:
            self.assertContains(response, f'name="{field}"')

    def test_create_project_saves_data_and_redirects(self):
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Aplikasi Catatan Kuliah",
                "category": "course",
                "description": "Aplikasi pencatat jadwal dan tugas kuliah.",
                "technologies": "Django, HTML5, CSS3",
                "started_at": "2026-09-01",
                "access_code": TEST_ACCESS_CODE,
            },
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(title="Aplikasi Catatan Kuliah").exists())

    def test_new_project_appears_on_projects_page(self):
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Aplikasi Catatan Kuliah",
                "category": "course",
                "description": "Aplikasi pencatat jadwal dan tugas kuliah.",
                "started_at": "2026-09-01",
                "access_code": TEST_ACCESS_CODE,
            },
            follow=True,
        )

        self.assertContains(response, "Aplikasi Catatan Kuliah")
        self.assertTrue(
            Project.objects.filter(title="Aplikasi Catatan Kuliah").exists()
        )

    def test_invalid_project_form_does_not_save(self):
        response = self.client.post(
            reverse("main:create_project"),
            {"title": "", "description": "", "started_at": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertEqual(Project.objects.count(), 1)

    def test_ended_at_before_started_at_is_rejected(self):
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Proyek Salah Tanggal",
                "description": "Proyek dengan periode terbalik.",
                "started_at": "2026-09-01",
                "ended_at": "2026-08-01",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tidak boleh lebih awal")
        self.assertFalse(Project.objects.filter(title="Proyek Salah Tanggal").exists())


class ProjectDataDeliveryTest(PortfolioTestCase):
    """Endpoint JSON/XML dan halaman projects yang membaca hasil deserialisasi."""

    def setUp(self):
        super().setUp()
        self.other_project = Project.objects.create(
            title="Game Visual Novel",
            description="Proyek game berbasis Ren'Py.",
            started_at=date(2025, 3, 1),
        )

    def test_projects_json_endpoint_returns_json(self):
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("application/json"))

        payload = json.loads(response.content.decode("utf-8"))
        titles = [item["fields"]["title"] for item in payload]
        self.assertIn(self.project.title, titles)

    def test_projects_json_endpoint_filters_by_title(self):
        response = self.client.get(
            reverse("main:get_projects_json"), {"title": "visual"}
        )

        payload = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["fields"]["title"], self.other_project.title)

    def test_projects_json_endpoint_returns_empty_list_when_no_match(self):
        response = self.client.get(
            reverse("main:get_projects_json"), {"title": "tidak ada"}
        )

        self.assertEqual(json.loads(response.content.decode("utf-8")), [])

    def test_projects_xml_endpoint_returns_xml(self):
        response = self.client.get(reverse("main:get_projects_xml"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("application/xml"))
        self.assertIn(self.project.title, response.content.decode("utf-8"))

    def test_projects_page_has_search_form(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, 'name="title"')

    def test_projects_page_filters_by_title(self):
        response = self.client.get(
            reverse("main:show_projects"), {"title": "visual"}
        )

        self.assertContains(response, self.other_project.title)
        self.assertNotContains(response, self.project.title)

    def test_projects_page_shows_message_when_filter_finds_nothing(self):
        response = self.client.get(
            reverse("main:show_projects"), {"title": "tidak ada"}
        )

        self.assertContains(response, "Tidak ada proyek dengan nama tersebut.")
        self.assertNotContains(response, self.project.title)
        self.assertNotContains(response, self.other_project.title)


@override_settings(PORTFOLIO_ACCESS_CODE=TEST_ACCESS_CODE)
class ProjectDeleteTest(PortfolioTestCase):
    def test_projects_page_shows_delete_modal(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, f'id="delete-project-{self.project.id}"')
        self.assertContains(
            response, f'popovertarget="delete-project-{self.project.id}"'
        )
        self.assertContains(response, "Hapus Proyek?")
        self.assertContains(response, 'name="access_code"')
        self.assertContains(
            response, reverse("main:delete_project", args=[self.project.id])
        )

    def test_delete_project_removes_data_and_redirects(self):
        response = self.client.post(
            reverse("main:delete_project", args=[self.project.id]),
            {"access_code": TEST_ACCESS_CODE},
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())
        self.assertEqual(Project.objects.count(), 0)

    def test_delete_project_only_works_with_post(self):
        response = self.client.get(
            reverse("main:delete_project", args=[self.project.id])
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())

    def test_delete_project_with_unknown_id_returns_404(self):
        response = self.client.post(
            reverse("main:delete_project", args=[uuid.uuid4()])
        )

        self.assertEqual(response.status_code, 404)


@override_settings(PORTFOLIO_ACCESS_CODE=TEST_ACCESS_CODE)
class AccessCodeTest(PortfolioTestCase):
    """Operasi tulis wajib pakai kode akses, lewat field form atau header."""

    def test_create_project_requires_code(self):
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Proyek Tanpa Kode",
                "category": "personal",
                "description": "Nggak boleh tersimpan.",
                "started_at": "2026-09-01",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kode akses wajib diisi.")
        self.assertFalse(Project.objects.filter(title="Proyek Tanpa Kode").exists())

    def test_create_project_rejects_wrong_code(self):
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Proyek Kode Ngawur",
                "category": "personal",
                "description": "Nggak boleh tersimpan.",
                "started_at": "2026-09-01",
                "access_code": "kode-ngawur",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kode akses salah.")
        self.assertFalse(
            Project.objects.filter(title="Proyek Kode Ngawur").exists()
        )

    def test_create_project_accepts_code_from_header(self):
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Proyek Lewat Header",
                "category": "personal",
                "description": "Dikirim pakai header X-Portfolio-Key.",
                "started_at": "2026-09-01",
            },
            headers={"X-Portfolio-Key": TEST_ACCESS_CODE},
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(title="Proyek Lewat Header").exists())

    def test_delete_project_rejects_wrong_code(self):
        response = self.client.post(
            reverse("main:delete_project", args=[self.project.id]),
            {"access_code": "kode-ngawur"},
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())

    def test_delete_project_accepts_code_from_header(self):
        response = self.client.post(
            reverse("main:delete_project", args=[self.project.id]),
            headers={"X-Portfolio-Key": TEST_ACCESS_CODE},
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())


@override_settings(PORTFOLIO_ACCESS_CODE="")
class AccessCodeNotConfiguredTest(PortfolioTestCase):
    """Fail-closed: tanpa kode di environment, semua request tulis ditolak."""

    def test_create_project_is_rejected(self):
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Proyek Tanpa Konfigurasi",
                "category": "personal",
                "description": "Ditolak karena kode akses belum di-set.",
                "started_at": "2026-09-01",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "belum dikonfigurasi")
        self.assertFalse(
            Project.objects.filter(title="Proyek Tanpa Konfigurasi").exists()
        )

    def test_delete_project_is_rejected(self):
        response = self.client.post(
            reverse("main:delete_project", args=[self.project.id])
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())


@override_settings(PORTFOLIO_ACCESS_CODE=TEST_ACCESS_CODE)
class ExperienceFormTest(PortfolioTestCase):
    """Form tambah & ubah pengalaman, termasuk proteksi kode aksesnya."""

    def test_create_experience_url_is_accessible(self):
        response = self.client.get(reverse("main:create_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")

    def test_create_experience_form_shows_fields(self):
        response = self.client.get(reverse("main:create_experience"))

        for field in [
            "title",
            "role",
            "organization",
            "description",
            "category",
            "started_at",
            "access_code",
        ]:
            self.assertContains(response, f'name="{field}"')

    def test_create_experience_saves_data_and_redirects(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Asisten Dosen DDPI",
                "role": "Teaching Assistant",
                "organization": "Fasilkom UI",
                "description": "Mendampingi praktikum dasar pemrograman.",
                "category": "part-time",
                "started_at": "2026-02-01",
                "access_code": TEST_ACCESS_CODE,
            },
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(
            Experience.objects.filter(title="Asisten Dosen DDPI").exists()
        )

    def test_new_experience_appears_on_experience_page(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Asisten Dosen DDPI",
                "role": "Teaching Assistant",
                "organization": "Fasilkom UI",
                "description": "Mendampingi praktikum dasar pemrograman.",
                "category": "part-time",
                "started_at": "2026-02-01",
                "access_code": TEST_ACCESS_CODE,
            },
            follow=True,
        )

        self.assertContains(response, "Asisten Dosen DDPI")
        self.assertTrue(
            Experience.objects.filter(title="Asisten Dosen DDPI").exists()
        )

    def test_invalid_experience_form_does_not_save(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {"title": "", "role": "", "description": "", "started_at": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertEqual(Experience.objects.count(), 1)

    def test_ended_at_before_started_at_is_rejected(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Pengalaman Salah Tanggal",
                "role": "Anggota",
                "description": "Periode terbalik.",
                "started_at": "2026-09-01",
                "ended_at": "2026-08-01",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tidak boleh lebih awal")
        self.assertFalse(
            Experience.objects.filter(title="Pengalaman Salah Tanggal").exists()
        )

    def test_update_experience_url_prefills_form(self):
        response = self.client.get(
            reverse("main:update_experience", args=[self.experience.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "Ubah Experience")
        self.assertContains(response, self.experience.title)

    def test_update_experience_saves_changes_and_redirects(self):
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Asisten Dosen PBP",
                "role": "Lead Teaching Assistant",
                "organization": "Fasilkom UI",
                "description": "Deskripsi baru hasil suntingan.",
                "category": "part-time",
                "started_at": "2025-08-01",
                "access_code": TEST_ACCESS_CODE,
            },
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.role, "Lead Teaching Assistant")
        self.assertEqual(
            self.experience.description, "Deskripsi baru hasil suntingan."
        )

    def test_update_experience_with_unknown_id_returns_404(self):
        response = self.client.get(
            reverse("main:update_experience", args=[uuid.uuid4()])
        )

        self.assertEqual(response.status_code, 404)

    def test_experience_page_shows_update_link(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(
            response, reverse("main:update_experience", args=[self.experience.id])
        )


@override_settings(PORTFOLIO_ACCESS_CODE=TEST_ACCESS_CODE)
class ExperienceDeleteTest(PortfolioTestCase):
    def test_experience_page_shows_delete_modal(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(
            response, f'id="delete-experience-{self.experience.id}"'
        )
        self.assertContains(
            response, f'popovertarget="delete-experience-{self.experience.id}"'
        )
        self.assertContains(response, "Hapus Experience?")
        self.assertContains(response, 'name="access_code"')
        self.assertContains(
            response, reverse("main:delete_experience", args=[self.experience.id])
        )

    def test_delete_experience_removes_data_and_redirects(self):
        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id]),
            {"access_code": TEST_ACCESS_CODE},
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertFalse(
            Experience.objects.filter(pk=self.experience.id).exists()
        )
        self.assertEqual(Experience.objects.count(), 0)

    def test_delete_experience_only_works_with_post(self):
        response = self.client.get(
            reverse("main:delete_experience", args=[self.experience.id])
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(
            Experience.objects.filter(pk=self.experience.id).exists()
        )

    def test_delete_experience_with_unknown_id_returns_404(self):
        response = self.client.post(
            reverse("main:delete_experience", args=[uuid.uuid4()])
        )

        self.assertEqual(response.status_code, 404)


class ExperienceDataDeliveryTest(PortfolioTestCase):
    """Endpoint JSON/XML pengalaman dan halaman yang membaca deserialisasi."""

    def test_experience_json_endpoint_returns_json(self):
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response["Content-Type"].startswith("application/json")
        )

        payload = json.loads(response.content.decode("utf-8"))
        titles = [item["fields"]["title"] for item in payload]
        self.assertIn(self.experience.title, titles)

    def test_experience_xml_endpoint_returns_xml(self):
        response = self.client.get(reverse("main:get_experience_xml"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("application/xml"))
        self.assertContains(response, self.experience.title)

    def test_experience_page_still_renders_after_json_round_trip(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.role)


@override_settings(PORTFOLIO_ACCESS_CODE=TEST_ACCESS_CODE)
class ExperienceAccessCodeTest(PortfolioTestCase):
    """Operasi tulis pengalaman wajib kode akses, lewat field atau header."""

    def test_create_experience_requires_code(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Pengalaman Tanpa Kode",
                "role": "Anggota",
                "description": "Nggak boleh tersimpan.",
                "started_at": "2026-02-01",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kode akses wajib diisi.")
        self.assertFalse(
            Experience.objects.filter(title="Pengalaman Tanpa Kode").exists()
        )

    def test_create_experience_rejects_wrong_code(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Pengalaman Kode Ngawur",
                "role": "Anggota",
                "description": "Nggak boleh tersimpan.",
                "started_at": "2026-02-01",
                "access_code": "kode-ngawur",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kode akses salah.")
        self.assertFalse(
            Experience.objects.filter(title="Pengalaman Kode Ngawur").exists()
        )

    def test_create_experience_accepts_code_from_header(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Pengalaman Lewat Header",
                "role": "Anggota",
                "description": "Dikirim pakai header X-Portfolio-Key.",
                "category": "volunteer",
                "started_at": "2026-02-01",
            },
            headers={"X-Portfolio-Key": TEST_ACCESS_CODE},
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(
            Experience.objects.filter(title="Pengalaman Lewat Header").exists()
        )

    def test_update_experience_rejects_wrong_code(self):
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Asisten Dosen PBP",
                "role": "Role Palsu",
                "organization": "Fasilkom UI",
                "description": "Gak boleh berubah.",
                "category": "part-time",
                "started_at": "2025-08-01",
                "access_code": "kode-ngawur",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.role, "Teaching Assistant")

    def test_update_experience_accepts_code_from_header(self):
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Asisten Dosen PBP",
                "role": "Lead Teaching Assistant",
                "organization": "Fasilkom UI",
                "description": "Lewat header.",
                "category": "part-time",
                "started_at": "2025-08-01",
            },
            headers={"X-Portfolio-Key": TEST_ACCESS_CODE},
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.role, "Lead Teaching Assistant")

    def test_delete_experience_rejects_wrong_code(self):
        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id]),
            {"access_code": "kode-ngawur"},
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(
            Experience.objects.filter(pk=self.experience.id).exists()
        )

    def test_delete_experience_accepts_code_from_header(self):
        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id]),
            headers={"X-Portfolio-Key": TEST_ACCESS_CODE},
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertFalse(
            Experience.objects.filter(pk=self.experience.id).exists()
        )


@override_settings(PORTFOLIO_ACCESS_CODE="")
class ExperienceAccessCodeNotConfiguredTest(PortfolioTestCase):
    """Fail-closed juga berlaku untuk operasi tulis pengalaman."""

    def test_create_experience_is_rejected(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Pengalaman Tanpa Konfigurasi",
                "role": "Anggota",
                "description": "Ditolak karena kode akses belum di-set.",
                "started_at": "2026-02-01",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "belum dikonfigurasi")
        self.assertFalse(
            Experience.objects.filter(
                title="Pengalaman Tanpa Konfigurasi"
            ).exists()
        )

    def test_delete_experience_is_rejected(self):
        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id])
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(
            Experience.objects.filter(pk=self.experience.id).exists()
        )
