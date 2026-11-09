from django.urls import path

from main.views import (
    create_project,
    delete_project,
    get_experience_json,
    get_experience_xml,
    get_projects_json,
    get_projects_xml,
    show_experience,
    show_main,
    show_projects,
    register,
    login_user,
    logout_user,
    toggle_star,
    create_project_ajax,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path(
        "projects/<uuid:project_id>/delete/",
        delete_project,
        name="delete_project",
    ),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("api/experience/xml/", get_experience_xml, name="get_experience_xml"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("api/projects/xml/", get_projects_xml, name="get_projects_xml"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
]