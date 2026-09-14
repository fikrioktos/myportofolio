from datetime import date

from django.test import TestCase
from django.urls import reverse

from main.models import Experience, Project


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
