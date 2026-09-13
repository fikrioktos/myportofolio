from datetime import date

from django.db import migrations

DATA = [
    {
        "title": "Interactive Educational Visual Novel",
        "category": "course",
        "description": (
            "Proyek akhir MPKT: membangun visual novel edukatif interaktif bersama tim "
            "sepuluh orang menggunakan Ren'Py. Bertanggung jawab pada pengujian fungsional "
            "dan naratif serta evaluasi konsistensi cerita dan pengalaman pengguna."
        ),
        "technologies": "Ren'Py, Python",
        "repository_url": None,
        "started_at": date(2026, 1, 1),
        "ended_at": date(2026, 6, 30),
    },
    {
        "title": "RAG Failure Analysis",
        "category": "research",
        "description": (
            "Riset tiga orang di RISTEK Data Science & AI untuk menganalisis failure mode "
            "sistem Retrieval-Augmented Generation. Mengimplementasikan dan mengevaluasi "
            "metode retrieval berbasis keyword (BM25) dan semantic pada dataset Indonesian "
            "TyDi QA, lalu melakukan evaluasi kuantitatif dan error analysis."
        ),
        "technologies": "Python, BM25, Semantic Retrieval, TyDi QA",
        "repository_url": None,
        "started_at": date(2026, 2, 1),
        "ended_at": None,
    },
    {
        "title": "Kompetisi Machine Learning Kaggle",
        "category": "competition",
        "description": (
            "Berlatih pemodelan machine learning melalui kompetisi Kaggle: eksplorasi data, "
            "rekayasa fitur, dan pemilihan model untuk kasus tabular."
        ),
        "technologies": "Python, Pandas, Scikit-learn, LightGBM",
        "repository_url": None,
        "started_at": date(2026, 3, 1),
        "ended_at": None,
    },
    {
        "title": "Website Portofolio PBP",
        "category": "personal",
        "description": (
            "Website portofolio pribadi yang dibangun dengan Django mengikuti alur "
            "Model-View-Template. Data experience dan project disimpan di database dan "
            "disajikan lewat template, bukan ditulis langsung di HTML."
        ),
        "technologies": "Django, HTML5, CSS3, PostgreSQL",
        "repository_url": "https://github.com/fikrioktos/myportofolio",
        "started_at": date(2026, 8, 31),
        "ended_at": None,
    },
]


def seed_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    for item in DATA:
        Project.objects.get_or_create(title=item["title"], defaults=item)


def unseed_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    Project.objects.filter(title__in=[item["title"] for item in DATA]).delete()


class Migration(migrations.Migration):
    dependencies = [("main", "0004_project")]

    operations = [migrations.RunPython(seed_projects, unseed_projects)]
