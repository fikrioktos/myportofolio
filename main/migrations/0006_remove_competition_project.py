from datetime import date

from django.db import migrations

TITLE = "Kompetisi Machine Learning Kaggle"

ORIGINAL = {
    "title": TITLE,
    "category": "competition",
    "description": (
        "Berlatih pemodelan machine learning melalui kompetisi Kaggle: eksplorasi data, "
        "rekayasa fitur, dan pemilihan model untuk kasus tabular."
    ),
    "technologies": "Python, Pandas, Scikit-learn, LightGBM",
    "repository_url": None,
    "started_at": date(2026, 3, 1),
    "ended_at": None,
}


def remove_competition_project(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    Project.objects.filter(title=TITLE).delete()


def restore_competition_project(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    Project.objects.get_or_create(title=TITLE, defaults=ORIGINAL)


class Migration(migrations.Migration):
    dependencies = [("main", "0005_seed_project_data")]

    operations = [migrations.RunPython(remove_competition_project, restore_competition_project)]
