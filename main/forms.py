from django import forms
from main.models import Project
class ProjectForm(forms.ModelForm):
    """Form tambah proyek, dibangun otomatis dari model Project."""
    class Meta:
        model = Project
        fields = [
            "title",
            "category",
            "description",
            "technologies",
            "repository_url",
            "report_url",
            "deployment_url",
            "started_at",
            "ended_at",
        ]
        labels = {
            "title": "Nama Proyek",
            "category": "Kategori",
            "description": "Deskripsi Proyek",
            "technologies": "Teknologi yang Digunakan",
            "repository_url": "URL Repositori",
            "report_url": "URL Laporan",
            "deployment_url": "URL Demo",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Website Portofolio PBP", "maxlength": 255}
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Ceritakan proyeknya", "rows": 4}
            ),
            "technologies": forms.TextInput(
                attrs={"placeholder": "Django, HTML5, CSS3"}
            ),
            "repository_url": forms.URLInput(
                attrs={"placeholder": "https://github.com/fikrioktos/myportofolio"}
            ),
            "report_url": forms.URLInput(
                attrs={"placeholder": "https://drive.google.com/file/d/..."}
            ),
            "deployment_url": forms.URLInput(
                attrs={"placeholder": "https://contoh-demo.com"}
            ),
            "started_at": forms.DateInput(attrs={"type": "date"}),
            "ended_at": forms.DateInput(attrs={"type": "date"}),
        }
    def clean(self):
        cleaned_data = super().clean()
        started_at = cleaned_data.get("started_at")
        ended_at = cleaned_data.get("ended_at")
        if started_at and ended_at and ended_at < started_at:
            self.add_error(
                "ended_at", "Tanggal selesai tidak boleh lebih awal dari tanggal mulai."
            )
        return cleaned_data