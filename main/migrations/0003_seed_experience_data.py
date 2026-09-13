from datetime import date

from django.db import migrations

EXPERIENCE_DATA = [
    {
        "title": "RISTEK Fasilkom UI",
        "role": "Member",
        "organization": "Data Science & AI Special Interest Group",
        "description": (
            "Selected through a competitive recruitment process. "
            "Conducted research on Retrieval-Augmented Generation (RAG) systems "
            "in a three-member team. Participated in technical study groups covering "
            "NLP, computer vision, deep learning, recommender systems, and MLOps."
        ),
        "category": "part-time",
        "started_at": date(2026, 1, 1),
        "ended_at": None,
    },
    {
        "title": "Teaching Assistant",
        "role": "Teaching Assistant",
        "organization": "Dasar-Dasar Pemrograman 1 · Fasilkom UI",
        "description": (
            "Teaching assistant for the introductory programming course at "
            "Faculty of Computer Science, Universitas Indonesia."
        ),
        "category": "part-time",
        "started_at": date(2026, 1, 1),
        "ended_at": None,
    },
    {
        "title": "BEM UI",
        "role": "Staff",
        "organization": "Bidang Keilmuan",
        "description": (
            "Staff of the Scientific Affairs division at Universitas Indonesia "
            "Student Executive Board."
        ),
        "category": "part-time",
        "started_at": date(2026, 1, 1),
        "ended_at": None,
    },
    {
        "title": "DDP 0 Fasilkom UI",
        "role": "Head of Mentor Division",
        "organization": "Bridging Program for New Students",
        "description": (
            "Led the administration and supervision of 166 mentors supporting "
            "475 mentees throughout a four-week mentoring program. Designed "
            "systematic administrative workflows for mentor management. "
            "Coordinated mentoring operations and communication across the "
            "organizing committee."
        ),
        "category": "part-time",
        "started_at": date(2026, 1, 1),
        "ended_at": date(2026, 6, 1),
    },
]


def seed_experience(apps, schema_editor):
    """Isi tabel Experience dengan data portofolio.

    Pakai get_or_create supaya migrasi ini idempotent: kalau datanya sudah ada
    (misalnya di database lokal), tidak akan dibuat duplikat.
    """
    Experience = apps.get_model("main", "Experience")

    for item in EXPERIENCE_DATA:
        _, created = Experience.objects.get_or_create(
            title=item["title"],
            defaults=item,
        )
        if created:
            print(f"  + Experience dibuat: {item['title']}")


def remove_seeded_experience(apps, schema_editor):
    """Kebalikan dari seed_experience, dipakai kalau migrasi di-rollback."""
    Experience = apps.get_model("main", "Experience")
    titles = [item["title"] for item in EXPERIENCE_DATA]
    Experience.objects.filter(title__in=titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_experience_organization_experience_role_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_experience, remove_seeded_experience),
    ]
