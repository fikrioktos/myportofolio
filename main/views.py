from django.contrib import messages
from django.shortcuts import redirect, render

from main.forms import ProjectForm
from main.models import Experience, Project


def show_main(request):
    context = {
        "name": "Fikri Okto Setiadi",
        "npm": "2506621655",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Fikri Okto Setiadi",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_projects(request):
    context = {
        "name": "Fikri Okto Setiadi",
        "project_list": Project.objects.all().order_by("-started_at"),
    }
    return render(request, "projects.html", context)

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proyek baru berhasil ditambahkan!")
            return redirect("main:show_projects")
    else:
        form = ProjectForm()

    context = {
        "name": "Fikri Okto Setiadi",
        "form": form,
    }
    return render(request, "projects_form.html", context)
