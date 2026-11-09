from datetime import date
import json
import uuid

from django.contrib.auth.models import User, Group
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
        # View tulis dikunci @login_required + is_superuser, jadi client test
        # harus login sebagai pemilik dulu.
        self.owner = User.objects.create_superuser(
            "pemilik", "pemilik@example.com", "pw-uji-123"
        )
        self.client.force_login(self.owner)

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

    def test_experience_page_renders_ajax_shell(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'id="experience-search-form"')
        self.assertContains(response, 'id="experience-grid"')
        self.assertContains(response, 'id="experience-loading"')
        self.assertContains(response, 'id="experience-empty"')
        self.assertContains(response, 'id="experience-error"')
        self.assertNotContains(response, self.experience.description)

    def test_empty_experience_json_returns_empty_list(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertEqual(json.loads(response.content.decode("utf-8")), [])

    def test_completed_experience_json_contains_end_date(self):
        self.experience.ended_at = date(2026, 6, 30)
        self.experience.save()
        response = self.client.get(reverse("main:get_experience_json"))
        payload = json.loads(response.content.decode("utf-8"))
        experience_data = next(
            item["fields"]
            for item in payload
            if item["pk"] == str(self.experience.id)
        )

        self.assertFalse(experience_data["is_ongoing"])
        self.assertEqual(experience_data["started_at"], "2025-08-01")
        self.assertEqual(experience_data["ended_at"], "2026-06-30")

    def test_experience_json_includes_organization_link(self):
        self.experience.organization_url = "https://bem.cs.ui.ac.id/"
        self.experience.save()
        response = self.client.get(reverse("main:get_experience_json"))
        payload = json.loads(response.content.decode("utf-8"))
        experience_data = next(
            item["fields"]
            for item in payload
            if item["pk"] == str(self.experience.id)
        )

        self.assertEqual(
            experience_data["organization_url"],
            "https://bem.cs.ui.ac.id/",
        )

    def test_experience_json_uses_null_for_missing_organization_link(self):
        response = self.client.get(reverse("main:get_experience_json"))
        payload = json.loads(response.content.decode("utf-8"))
        experience_data = next(
            item["fields"]
            for item in payload
            if item["pk"] == str(self.experience.id)
        )

        self.assertIsNone(experience_data["organization_url"])


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

    def test_projects_page_contains_ajax_containers(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, 'id="project-search-form"')
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, 'id="empty"')
        self.assertNotContains(response, self.project.description)

    def test_empty_projects_json_returns_empty_list(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(json.loads(response.content.decode("utf-8")), [])

    def test_projects_json_includes_external_links(self):
        self.project.report_url = "https://drive.google.com/file/d/contoh/view"
        self.project.deployment_url = "https://contoh.itch.io/game"
        self.project.save()
        response = self.client.get(reverse("main:get_projects_json"))

        payload = json.loads(response.content.decode("utf-8"))
        project_data = next(
            item["fields"] for item in payload if item["pk"] == str(self.project.id)
        )
        self.assertEqual(project_data["repository_url"], self.project.repository_url)
        self.assertEqual(project_data["report_url"], self.project.report_url)
        self.assertEqual(project_data["deployment_url"], self.project.deployment_url)

    def test_projects_page_uses_ajax_card_builder(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "const links = [")
        self.assertContains(response, "Lihat laporan")
        self.assertContains(response, "Coba demo")


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

    def test_new_project_appears_in_projects_json(self):
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Aplikasi Catatan Kuliah",
                "category": "course",
                "description": "Aplikasi pencatat jadwal dan tugas kuliah.",
                "started_at": "2026-09-01",
                "access_code": TEST_ACCESS_CODE,
            },
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        payload = json.loads(
            self.client.get(reverse("main:get_projects_json")).content.decode("utf-8")
        )
        titles = [item["fields"]["title"] for item in payload]
        self.assertIn("Aplikasi Catatan Kuliah", titles)

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


@override_settings(PORTFOLIO_ACCESS_CODE=TEST_ACCESS_CODE)
class ProjectAjaxCreateTest(PortfolioTestCase):
    """Endpoint tambah proyek AJAX dan pembersihan inputnya."""

    def ajax_payload(self, **overrides):
        payload = {
            "title": "Proyek AJAX",
            "category": "personal",
            "description": "Dibuat tanpa reload halaman.",
            "technologies": "Django, JavaScript",
            "started_at": "2026-09-01",
            "access_code": TEST_ACCESS_CODE,
        }
        payload.update(overrides)
        return payload

    def test_ajax_create_only_accepts_post(self):
        response = self.client.get(reverse("main:create_project_ajax"))

        self.assertEqual(response.status_code, 405)

    def test_ajax_create_rejects_anonymous_user_with_json(self):
        self.client.logout()
        response = self.client.post(
            reverse("main:create_project_ajax"), self.ajax_payload()
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response["Content-Type"].startswith("application/json"))
        self.assertEqual(
            json.loads(response.content.decode("utf-8"))["message"],
            "Hanya pemilik portofolio yang dapat menambahkan proyek.",
        )
        self.assertFalse(Project.objects.filter(title="Proyek AJAX").exists())

    def test_ajax_create_saves_valid_project_and_returns_json(self):
        response = self.client.post(
            reverse("main:create_project_ajax"), self.ajax_payload()
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response["Content-Type"].startswith("application/json"))
        body = json.loads(response.content.decode("utf-8"))
        project = Project.objects.get(title="Proyek AJAX")
        self.assertEqual(body["pk"], str(project.id))
        self.assertEqual(body["message"], "Proyek berhasil ditambahkan.")

    def test_ajax_create_rejects_html_only_title(self):
        response = self.client.post(
            reverse("main:create_project_ajax"),
            self.ajax_payload(title="<img src=x onerror=alert(1)>"),
        )

        self.assertEqual(response.status_code, 400)
        errors = json.loads(response.content.decode("utf-8"))["errors"]
        self.assertEqual(
            errors["title"][0]["message"],
            "Nama proyek tidak boleh hanya berisi tag HTML.",
        )
        self.assertFalse(Project.objects.filter(title__contains="img src").exists())

    def test_ajax_create_strips_html_from_text_fields(self):
        response = self.client.post(
            reverse("main:create_project_ajax"),
            self.ajax_payload(
                title="Proyek <b>AJAX</b>",
                description="Halo <b>dunia</b>",
                technologies="JavaScript <i>aman</i>",
            ),
        )

        self.assertEqual(response.status_code, 201)
        project = Project.objects.get(title="Proyek AJAX")
        self.assertEqual(project.description, "Halo dunia")
        self.assertEqual(project.technologies, "JavaScript aman")


class ProjectDataDeliveryTest(PortfolioTestCase):
    """Endpoint JSON/XML dan halaman projects yang membaca hasil deserialisasi."""

    def setUp(self):
        super().setUp()
        self.other_project = Project.objects.create(
            title="Game Visual Novel",
            description="Proyek game berbasis Ren'Py.",
            started_at=date(2025, 3, 1),
        )


    def test_api_does_not_leak_sensitive_fields(self):
        """Endpoint publik tidak menyebarkan kolom sensitif milik user."""
        for url in [
            reverse("main:get_projects_json"),
            reverse("main:get_experience_json"),
        ]:
            body = self.client.get(url).content.decode()
            self.assertNotIn("password", body)
            self.assertNotIn("last_login", body)
            

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

    def test_projects_page_keeps_search_query_for_ajax(self):
        response = self.client.get(
            reverse("main:show_projects"), {"title": "visual"}
        )

        self.assertContains(response, 'value="visual"')
        self.assertContains(response, 'id="grid"')
        self.assertNotContains(response, self.other_project.title)

    def test_projects_json_returns_empty_list_for_missing_title(self):
        response = self.client.get(
            reverse("main:get_projects_json"), {"title": "tidak ada"}
        )

        self.assertEqual(json.loads(response.content.decode("utf-8")), [])


@override_settings(PORTFOLIO_ACCESS_CODE=TEST_ACCESS_CODE)
class ProjectDeleteTest(PortfolioTestCase):
    def test_projects_page_includes_ajax_delete_template(self):
        # Tutorial 7: delete sekarang lewat API DRF (tombol data-action +
        # confirm), bukan lagi form access_code inline dari Tutorial 5.
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, 'data-action="delete"')
        self.assertContains(response, "Yakin ingin menghapus project ini?")
        self.assertNotContains(
            response,
            reverse(
                "main:delete_project",
                args=[uuid.UUID("00000000-0000-0000-0000-000000000000")],
            ),
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


class ExperienceDataDeliveryTest(PortfolioTestCase):
    """Endpoint JSON/XML Experience dan shell AJAX-nya."""

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

    def test_experience_page_contains_ajax_card_builder(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'src="/static/js/experience.js"')
        self.assertContains(response, "window.experienceConfig")
        self.assertNotContains(response, self.experience.description)


class ExperienceRoleRenderTest(PortfolioTestCase):
    """Halaman Experience menampilkan kontrol sesuai peran; hak aslinya dijaga API."""

    def setUp(self):
        super().setUp()
        from django.test import Client

        self.editor = User.objects.create_user("edito", email="e@e.com")
        Group.objects.get_or_create(name="Editor")[0].user_set.add(self.editor)
        self.editor_client = Client()
        self.editor_client.force_login(self.editor)

        self.plain_user = User.objects.create_user("biasa", email="b@e.com")
        self.plain_client = Client()
        self.plain_client.force_login(self.plain_user)

    def test_editor_sees_edit_modal_but_no_add_button(self):
        response = self.editor_client.get(reverse("main:show_experience"))

        self.assertContains(response, "canEdit: true")
        self.assertContains(response, "isSuperuser: false")
        self.assertContains(response, 'id="experience-form-modal"')
        self.assertNotContains(response, "experience-add-button")

    def test_plain_user_sees_neither_edit_modal_nor_add_button(self):
        response = self.plain_client.get(reverse("main:show_experience"))

        self.assertContains(response, "canEdit: false")
        self.assertNotContains(response, 'id="experience-form-modal"')
        self.assertNotContains(response, "experience-add-button")

    def test_owner_sees_add_button_and_edit_modal(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "isSuperuser: true")
        self.assertContains(response, "experience-add-button")
        self.assertContains(response, 'id="experience-form-modal"')
