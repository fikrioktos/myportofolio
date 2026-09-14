import uuid
from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='part-time')
    thumbnail = models.URLField(blank=True, null=True)
    organization_url = models.URLField(
        blank=True,
        null=True,
        help_text="Situs resmi organisasi atau kepanitiaan, mis. https://bem.cs.ui.ac.id/",
    )
    started_at = models.DateField()
    ended_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Project(models.Model):
    PROJECT_CATEGORIES = [
        ('research', 'Research'),
        ('course', 'Course Project'),
        ('competition', 'Competition'),
        ('personal', 'Personal'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=PROJECT_CATEGORIES, default='personal')
    description = models.TextField()
    technologies = models.CharField(max_length=255, blank=True)
    repository_url = models.URLField(blank=True, null=True)
    report_url = models.URLField(
        blank=True,
        null=True,
        help_text="Tautan laporan, makalah, atau technical report proyek.",
    )
    deployment_url = models.URLField(
        blank=True,
        null=True,
        help_text="Tautan versi live atau demo proyek yang bisa dicoba.",
    )
    started_at = models.DateField()
    ended_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None

