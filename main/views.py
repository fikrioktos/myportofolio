from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ProjectForm, access_code_error
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


def _projects_matching_query(request):
    """Ambil daftar proyek beserta kata kunci pencarian ?title= dari URL.

    Dipakai bersama oleh endpoint JSON, endpoint XML, dan halaman projects,
    supaya aturan filter hanya ditulis satu kali.
    """
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all().order_by("-started_at")

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    return projects, title_query


def get_projects_json(request):
    projects, _ = _projects_matching_query(request)
    projects_json = serializers.serialize("json", projects)

    return HttpResponse(projects_json, content_type="application/json")


def get_projects_xml(request):
    projects, _ = _projects_matching_query(request)
    projects_xml = serializers.serialize("xml", projects)

    return HttpResponse(projects_xml, content_type="application/xml")


def show_projects(request):
    json_response = get_projects_json(request)
    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]

    _, title_query = _projects_matching_query(request)

    context = {
        "name": "Fikri Okto Setiadi",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def create_project(request):
    if request.method == "POST":
        data = request.POST.copy()

        # Request dari curl/Postman bisa mengirim kode akses lewat header, jadi
        # field password di form tidak perlu diisi.
        header_code = request.headers.get("X-Portfolio-Key")
        if header_code:
            data["access_code"] = header_code

        form = ProjectForm(data)
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


def _supplied_access_code(request):
    """Kode akses datang lewat header X-Portfolio-Key atau field form."""
    return request.headers.get("X-Portfolio-Key") or request.POST.get(
        "access_code", ""
    )


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        error = access_code_error(_supplied_access_code(request))

        if error:
            messages.error(request, error)
            return redirect("main:show_projects")

        project.delete()
        messages.success(request, "Proyek berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")
