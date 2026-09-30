from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from main.forms import ExperienceForm, ProjectForm, access_code_error
from main.models import Experience, Project


def is_editor(user):
    """Anggota Django Group 'Editor' — grubnya dibuat lewat /admin."""
    return user.groups.filter(name="Editor").exists()


def can_edit_entry(user):
    """Boleh mengubah entri: pemilik (superuser) atau editor."""
    return user.is_superuser or is_editor(user)


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Fikri Okto Setiadi",
        "npm": "2506621655",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experience_json(request)
    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]

    context = {
        "name": "Fikri Okto Setiadi",
        "experience_list": experiences,
        "can_edit": can_edit_entry(request.user),
    }
    return render(request, "experience.html", context)


def _experiences_list(request):
    """Daftar pengalaman yang dikirim ke endpoint JSON/XML dan halaman."""
    return Experience.objects.all().order_by("-started_at")


def get_experience_json(request):
    experiences_json = serializers.serialize("json", _experiences_list(request), use_natural_foreign_keys=True)

    return HttpResponse(experiences_json, content_type="application/json")


def get_experience_xml(request):
    experiences_xml = serializers.serialize("xml", _experiences_list(request), use_natural_foreign_keys=True)

    return HttpResponse(experiences_xml, content_type="application/xml")


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
    projects = projects.prefetch_related("starred_by")

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "category": project.get_category_display(),
                "technologies": project.technologies,
                "repository_url": project.repository_url,
                "report_url": project.report_url,
                "deployment_url": project.deployment_url,
                "started_at": str(project.started_at),
                "ended_at": str(project.ended_at) if project.ended_at else None,
                "is_ongoing": project.is_ongoing,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)


def get_projects_xml(request):
    projects, _ = _projects_matching_query(request)
    projects_xml = serializers.serialize("xml", projects, use_natural_foreign_keys=True)

    return HttpResponse(projects_xml, content_type="application/xml")


def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Fikri Okto Setiadi",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "projects.html", context)


@login_required(login_url="/login/")
def create_project(request):

    if not request.user.is_superuser:
        raise PermissionDenied
    
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


@login_required(login_url="/login/")
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        error = access_code_error(_supplied_access_code(request))

        if error:
            messages.error(request, error)
            return redirect("main:show_projects")

        project.delete()
        messages.success(request, "Proyek berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == "POST":
        data = request.POST.copy()

        # Request dari curl/Postman bisa mengirim kode akses lewat header, jadi
        # field password di form tidak perlu diisi.
        header_code = request.headers.get("X-Portfolio-Key")
        if header_code:
            data["access_code"] = header_code

        form = ExperienceForm(data)
        if form.is_valid():
            form.save()
            messages.success(request, "Pengalaman baru berhasil ditambahkan!")
            return redirect("main:show_experience")
    else:
        form = ExperienceForm()

    context = {
        "name": "Fikri Okto Setiadi",
        "form": form,
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if not can_edit_entry(request.user):
        raise PermissionDenied

    if request.method == "POST":
        data = request.POST.copy()

        # Request dari curl/Postman bisa mengirim kode akses lewat header, jadi
        # field password di form tidak perlu diisi.
        header_code = request.headers.get("X-Portfolio-Key")
        if header_code:
            data["access_code"] = header_code

        form = ExperienceForm(data, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, "Pengalaman berhasil diperbarui!")
            return redirect("main:show_experience")
    else:
        form = ExperienceForm(instance=experience)

    context = {
        "name": "Fikri Okto Setiadi",
        "form": form,
        "experience": experience,
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        error = access_code_error(_supplied_access_code(request))

        if error:
            messages.error(request, error)
            return redirect("main:show_experience")

        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Fikri Okto Setiadi",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Fikri Okto Setiadi",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response


# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")


@login_required(login_url="/login/")
def toggle_experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")


@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

