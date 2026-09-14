"""Isi tautan eksternal untuk baris Experience dan Project yang sudah ada.

PWS tidak menyediakan shell atau console, jadi pengisian data ke database
production harus lewat migrasi. Migrasi ini idempotent: memakai update()
berdasarkan judul, sehingga aman dijalankan berulang dan tidak pernah membuat
baris duplikat.
"""

from django.db import migrations

EXPERIENCE_LINKS = {
    "RISTEK Fasilkom UI": "https://www.ristek.cs.ui.ac.id",
    "DDP 0 Fasilkom UI": "https://ddp0.csui.dev",
    "BEM UI": "https://bem.cs.ui.ac.id/",
    "Teaching Assistant": "https://cs.ui.ac.id",
}

PROJECT_LINKS = {
    "Interactive Educational Visual Novel": {
        "report_url": (
            "https://drive.google.com/file/d/1UtcfWXjAXR13z_E-YprtPqSUsl-TmXf5/view"
        ),
        "deployment_url": "https://rifkypadjri.itch.io/final-project-mpkt",
    },
    "RAG Failure Analysis": {
        "report_url": (
            "https://drive.google.com/file/d/1UZNI35qsRv67pJMzDqqqyKOk7OYu6shq/view"
        ),
    },
}


def add_links(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")
    Project = apps.get_model("main", "Project")

    for title, url in EXPERIENCE_LINKS.items():
        updated = Experience.objects.filter(title=title).update(organization_url=url)
        print(f"  ~ Experience '{title}': {updated} baris")

    for title, links in PROJECT_LINKS.items():
        updated = Project.objects.filter(title=title).update(**links)
        print(f"  ~ Project '{title}': {updated} baris")


def remove_links(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")
    Project = apps.get_model("main", "Project")

    Experience.objects.filter(title__in=EXPERIENCE_LINKS).update(organization_url=None)
    Project.objects.filter(title__in=PROJECT_LINKS).update(
        report_url=None, deployment_url=None
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_experience_organization_url_project_deployment_url_and_more"),
    ]

    operations = [
        migrations.RunPython(add_links, remove_links),
    ]