from django.contrib import admin

from main.models import Experience, Project


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'role', 'organization', 'category', 'started_at', 'ended_at')
    list_filter = ('category',)
    search_fields = ('title', 'role', 'organization')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'technologies', 'started_at', 'ended_at')
    list_filter = ('category',)
    search_fields = ('title', 'technologies')